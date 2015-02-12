__author__ = 'kamal'
from django import forms
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from cartoview2.catalog.models import Url
from django.templatetags.static import static
from django.core.urlresolvers import reverse

class ResourceURLWidget(forms.URLInput):
    def __init__(self, attrs=None):
        #choices = attrs.pop('choices', [])
        #self.choices = list(choices)
        super(ResourceURLWidget, self).__init__(attrs)


    def render(self, name, value, attrs=None):
        input_field = super(ResourceURLWidget, self).render(name, value, attrs)
        context = {
            "REST_URL": reverse("cartoview2_rest_url"),
            "STATIC_URL":static(""),
            'modal_id': attrs['id'] + "-modal",
            "url_field_id": attrs['id']
        }
        context.update(self.attrs)
        context.update(locals())
        field_html = render_to_string('catalog/fields/resource_url_field.html', context)
        modal_html = render_to_string('catalog/fields/resource_url_modal.html', context)
        return field_html + modal_html

class ResourceURLField(forms.URLField):
    widget = ResourceURLWidget
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        self.show_filter = kwargs.pop('show_filter', False)
        self.url_type = kwargs.pop('url_type', None)
        self.provider = kwargs.pop('provider', None)
        self.service_type = kwargs.pop('service_type', None)
        self.callback = kwargs.pop('callback', None)
        self.modal_id = kwargs.pop('modal_id', None)
        super(ResourceURLField, self).__init__(max_length, min_length, *args, **kwargs)


    def widget_attrs(self, widget):
        attrs = super(ResourceURLField, self).widget_attrs(widget)
        attrs["show_filter"] = self.show_filter
        attrs["url_type"] = self.url_type
        attrs["provider"] = self.provider
        attrs["service_type"] = self.service_type
        if self.modal_id:
            attrs["modal_id"] = self.modal_id
        if self.callback:
            attrs['callback'] = self.callback

        return attrs

class ResourceURL(models.URLField):
    def __init__(self, *args, **kwargs):
        #kwargs['max_length'] = kwargs.get('max_length', 200)


        super(ResourceURL, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': ResourceURLField}
        defaults.update(kwargs)
        return super(ResourceURL, self).formfield(**defaults)

    def get_choices(self, include_blank=None, blank_choice=None):
        choices = []
        urls = Url.objects.all()
        if self.url_type:
            urls = self.urls.filter(url_type=self.url_type)
        for url in urls:
            choices.append((url.url, url.url_label,))
        return choices