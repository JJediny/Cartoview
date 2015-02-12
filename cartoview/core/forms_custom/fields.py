# coding=utf-8

from django.forms import fields
from django.core.exceptions import ValidationError

import widgets as widgets_custom


class RangeFieldMixin(object):
    """ set validator for range MultiValueField """

    default_error_messages = {'invalid': u'Date format error',
                              'invalid_order': u'Invalid order',
                              'not_all_filled': u'Not all widget filled'}

    def validate(self, value):
        if (value[0] is None and value[1] is not None) or \
                (value[0] is not None and value[1] is None):
            raise ValidationError(self.default_error_messages['not_all_filled'])

        if value[0] and value[1] and value[0] > value[1]:
            raise ValidationError(self.default_error_messages['invalid_order'])

    def compress(self, data_list):
        return data_list


class DateRangeField(RangeFieldMixin, fields.MultiValueField):


    widget = widgets_custom.DateRangeWidget
    hidden_widget = widgets_custom.DateRangeHiddenWidget

    def __init__(self, input_date_formats=None, *args, **kwargs):
        
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])

        localize = kwargs.get('localize', False)

        fields_ = (fields.DateField(input_formats=input_date_formats,
                                    error_messages={'invalid': errors['invalid']},
                                    localize=localize),
                   fields.DateField(input_formats=input_date_formats,
                                    error_messages={'invalid': errors['invalid']},
                                    localize=localize),
        )
        super(DateRangeField, self).__init__(fields_, *args, **kwargs)

    def compress(self, data_list):
        return data_list


class NumberRangeField(RangeFieldMixin, fields.MultiValueField):
    
    widget = widgets_custom.NumberRangeWidget
    hidden_widget = widgets_custom.NumberRangeHiddenWidget

    def __init__(self, max_value=None, min_value=None, decimal_places=None, *args, **kwargs):
        
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        
        localize = kwargs.get('localize', False)

        fields_ = (fields.DecimalField(max_value=max_value,
                                       min_value=min_value,
                                       decimal_places=decimal_places,
                                       error_messages={'invalid': errors['invalid']},
                                       localize=localize),
                   fields.DecimalField(max_value=max_value,
                                       min_value=min_value,
                                       decimal_places=decimal_places,
                                       error_messages={'invalid': errors['invalid']},
                                       localize=localize),
        )
        super(NumberRangeField, self).__init__(fields_, *args, **kwargs)


