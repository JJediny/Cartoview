from django import forms
from form_utils.forms import BetterForm
from django.utils.translation import ugettext, ugettext_lazy as _
from cartoview2.core.models import *

from django.forms.models import model_to_dict
from django.forms.formsets import formset_factory
from django.contrib.auth.models import Group, User
from cartoview2.core.utils import get_permitted
from forms_custom.widgets import SelectMultipleAutocomplete

class KeyValueForm(BetterForm):
    def add_fields(self, groups):
        j=0
        data = {}
        fieldsets = []
        for group in groups:
            prefix = '%sobjects[%d].' % (self.field_name_prefix, j)
            name = '%sid' % prefix
            self.fields[name] = forms.IntegerField(widget= forms.HiddenInput())
            data[name] = group.pk
            name = '%sname' % prefix
            self.fields[name] = forms.CharField(widget= forms.HiddenInput())
            data[name] = group.name
            i = 0
            fields = []
            for item in group.keyvalue_set.all().order_by('id') :
                prefix = '%sobjects[%d].values[%d].' % (self.field_name_prefix, j, i)
                name = '%sid' % prefix
                self.fields[name] = forms.IntegerField(widget= forms.HiddenInput())
                data[name] = item.id
                fields.append(name)
                #self.fields['%skey' % prefix] = forms.CharField(widget= forms.HiddenInput())
                #data['%skey' % prefix] = item.key
                name = '%svalue' % prefix
                self.fields[name] = forms.CharField(label=item.key)
                data[name] = item.value
                fields.append( name)
                i += 1
            j += 1
            fieldset = (group.name,{'fields':fields})
            fieldsets.append(fieldset)
            self.initial = data
            if len(fieldsets) > 1:
                self._fieldsets = fieldsets


    def __init__(self, *args, **kwargs):
        field_name_prefix = kwargs.pop('field_name_prefix','')
        group_name= kwargs.pop('group_name',None)
        groups = kwargs.pop('groups',None)
        self.field_name_prefix = field_name_prefix if field_name_prefix == '' else field_name_prefix + '.'
        super(type(self), self).__init__(*args, **kwargs)
        self._row_attr = {}
        if group_name:
            group = KeyValueGroup.objects.get(name=group_name)
            self.add_fields([group])
        elif groups:
            self.add_fields(groups)
        else:
            self.add_fields(KeyValueGroup.objects.all())


    class Meta:
        pass

class TastypieForm(forms.Form):
    def __init__(self, *args, **kwargs):
        schema = kwargs.pop('schema')
        super(type(self), self).__init__(*args, **kwargs)

        for i, field_name in enumerate(schema['fields']):
            field = schema['fields'][field_name]
            if field['type'] == 'string':
                self.fields[field_name] = forms.CharField()


class AppInstallerForm(forms.ModelForm):
    error_messages = {
        'duplicate_app_name': _("An application with the same user has already installed."),
        'invalid_package_file': _("The uploaded file is not an application package."),
    }
    package_file = forms.FileField()

    class Meta:
        model = App
        fields = ("package_file",)

class AppForm (forms.ModelForm):
    class Meta:
        model = App
        fields = ("title","app_img","app_logo",)


class HomePageForm (forms.Form):

    homepage = forms.ModelChoiceField(queryset=HomePage.objects.all(),required=False)
    def __init__(self, *args, **kwargs):
        super(HomePageForm, self).__init__(*args, **kwargs)
        self.fields['homepage'].empty_label = None
    def save(self):
        data = self.cleaned_data
        if (data['homepage']):
            selected_homepage = data['homepage'].name
            home_keyvalue,created=KeyValue.objects.get_or_create(key='homepage')
            home_keyvalue.value= selected_homepage
            home_keyvalue.save()
from django.contrib.auth import get_user_model
qs = get_user_model().objects.all()
class PermissionsForm (forms.Form):
    perm_choices = (('admin', 'Admins only',), ('registered', 'All registered users',),('specific','Specific users'))
    permitted = forms.ChoiceField(widget=forms.RadioSelect, choices=perm_choices ,required=False,label='')
    permitted_users = forms.ModelMultipleChoiceField(queryset=qs,required= False , widget=SelectMultipleAutocomplete(queryset=qs,
                                                    expression="username__startswith"))
    title = ''
    perm = None
    def __init__(self, *args, **kwargs):
        super(PermissionsForm, self).__init__(*args, **kwargs)
        self.perm = self.initial
        self.initial = model_to_dict(self.perm)
        kwargs['prefix'] = self.perm.codename
        self.base_fields['permitted_users'].help_text = None

        #users = User.objects.filter( Q(user_permissions=perm) ).distinct()
        users , group = get_permitted(self.perm)
        self.title = self.perm.name
        if (group):
            self.fields['permitted'].initial = group.name
        elif (users):
            self.fields['permitted'].initial = 'specific'
            self.fields['permitted_users'].initial = users
    def clean_permitted_users(self):
        data = self.cleaned_data
        permitted_users = data['permitted_users']
        if ((data['permitted'] == 'specific') and (len(data['permitted_users'])== 0)):
             raise forms.ValidationError("At least one user must be selected.")
        else:
            return permitted_users
    def save(self):
        self.perm.group_set.clear()
        self.perm.user_set.clear()
        data = self.cleaned_data
        if (data['permitted'] == 'registered'):
            registered_group = Group.objects.get(name='registered')
            registered_group.permissions.add(self.perm)
        elif (data['permitted'] == 'admin'):
            admin_group = Group.objects.get(name='admin')
            admin_group.permissions.add(self.perm)

        else :
            # if len(data['permitted_users'])== 0:
            #     raise forms.ValidationError("At least one column must be selected to be appear in the grid.")
            # else:
            for user in data['permitted_users']:
                user.user_permissions.add(self.perm)

permissions_formset = formset_factory(PermissionsForm, extra=0)

class SettingsForm (forms.ModelForm):
    show_home_logo = forms.BooleanField( required =False,label='Show home logo on side menu')
    class Meta:
        model = Settings
        exclude = ['site']