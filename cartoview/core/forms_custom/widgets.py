# coding=utf-8
import datetime

from django import forms
from django.db import connection
from django.forms import widgets as widgets_django
from django.forms import fields
from django.template.loader import render_to_string
from django.forms.widgets import HiddenInput
import pickle


class DateRangeWidget(widgets_django.MultiWidget):
    def __init__(self, attrs={}, date_format=None):
        attrs = dict(attrs, **{'class': 'date form-control'})

        widgets = (fields.DateInput(attrs=attrs),
                   fields.DateInput(attrs=attrs))

        super(DateRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value
        return [None, None]


class DateRangeHiddenWidget(DateRangeWidget):
    is_hidden = True

    def __init__(self, attrs={}, date_format=None):
        super(DateRangeHiddenWidget, self).__init__(attrs, date_format)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class NumberRangeWidget(widgets_django.MultiWidget):
    def __init__(self, attrs={}):
        attrs = dict(attrs, **{'class': 'number form-control'})

        widgets = (forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs))
        super(NumberRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [str(value[0]), str(value[1])]
        return [None, None]


class NumberRangeHiddenWidget(NumberRangeWidget):
    is_hidden = True

    def __init__(self, attrs={}):
        super(NumberRangeHiddenWidget, self).__init__(attrs)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class SplitDateTimeWidget(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None, date_class='date', time_class='time'):
        date_attrs = attrs.copy()
        date_attrs['class'] = date_class

        time_attrs = attrs.copy()
        time_attrs['class'] = time_class

        widgets = (fields.DateInput(attrs=date_attrs, format=date_format),
                   fields.TimeInput(attrs=time_attrs, format=time_format))

        forms.MultiWidget.__init__(self, widgets=widgets, attrs=attrs)


class TreeWidget(widgets_django.Select):
    
    def __init__(self, queryset, attrs=None):
        super(TreeWidget, self).__init__(attrs)
        self._queryset = queryset

    def render(self, name, value, attrs=None, choices=()):
        if value:
            value = self._queryset.get(id=value)

        application = self._queryset.model.__module__.split('.')[-0]
        model_name = self._queryset.model.__name__

        return render_to_string('forms_custom/tree_widget.html', {'attrs': attrs, 'value': value,
                                                                  'name': name, 'application': application,
                                                                  'model_name': model_name})


class AutocompleteWidgetMixin(object):

    def _parse_queryset(self):

        self._application = self._queryset.model.__module__.split('.')[-0]
        self._model_name = self._queryset.model.__name__
        
        where_node = self._queryset.query.__dict__['where']
        where, where_params = where_node.as_sql(connection.ops.quote_name, connection)
        
        if where:
            self._queryset_where = where.replace('"', '\"')
            self._queryset_where_params = pickle.dumps(where_params)
        else:
            self._queryset_where = ""
            self._queryset_where_params = ""


class SelectAutocomplete(widgets_django.Select, AutocompleteWidgetMixin):
    
    def __init__(self, queryset, attrs=None):
        super(SelectAutocomplete, self).__init__(attrs)
        self._queryset = queryset
        self._parse_queryset()

    def render(self, name, value, attrs=None, choices=()):
        
        application = self._queryset.model.__module__.split('.')[-0]
        model_name = self._queryset.model.__name__

        return render_to_string('forms_custom/autocomplete.html', {'value': value, 
            'attrs': attrs,
            'application': application,
            'model_name': model_name,
            'expression': 'title__startswith',
            'name': name,
            'where': self._queryset_where,
            'where_params': self._queryset_where_params
        })


class SelectMultipleAutocomplete(widgets_django.SelectMultiple, AutocompleteWidgetMixin):

    def __init__(self, queryset, attrs=None, expression='title__startswith'):
        
        super(SelectMultipleAutocomplete, self).__init__(attrs)
        self._queryset = queryset
        self._expression = expression
        self._parse_queryset()

    def render(self, name, value, attrs=None, choices=()):

        return render_to_string('forms_custom/autocomplete_multiple.html', {'value': value, 
            'attrs': attrs,
            'application': self._queryset.model._meta.app_label,
            'model_name': self._model_name,
            'expression': self._expression,
            'name': name,
            'where': self._queryset_where,
            'where_params': self._queryset_where_params
        })

    def value_from_datadict(self, data, files, name):
        """ replace scalar value ("1,2,3") to list ([1,2,3])"""

        data_dict = super(SelectMultipleAutocomplete, self).value_from_datadict(data, files, name)
        if (len(data_dict)>0):
            value = data_dict[0]
            return value.split(",")
        return None
        
