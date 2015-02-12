from django import forms
from allauth.socialaccount.models import *
from form_utils.forms import BetterForm
from django.forms import ModelForm,Form
from form_utils.forms import BetterForm
from models import Settings
# class SocialAppForm(ModelForm):
#     class Meta:
#         model = SocialApp
#         fields=('id','client_id','secret')


class SocialAppForm(Form):
    def __init__(self,prefix,*args, **kwargs):
        super(SocialAppForm, self).__init__(*args, **kwargs)
        self.fields[prefix + '.id'] = forms.CharField(widget=forms.HiddenInput())
        self.fields[prefix + '.client_id'] = forms.CharField( label="API ID")
        self.fields[prefix + '.secret'] = forms.CharField(label="API Secret key")

class SettingsForm (forms.ModelForm):
    enable_social = forms.BooleanField( required =False,label='Enable social registration')
    class Meta:
        model = Settings
        exclude = ['site']