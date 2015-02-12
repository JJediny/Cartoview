__author__ = 'kamal'

import json
from django.conf import settings
from django import template
import os
from django.utils.safestring import mark_safe
from django.templatetags.static import static
register = template.Library()


@register.inclusion_tag('leaflet_style/styler_css.html')
def leaflet_styler_css():
    css_files = ['leaflet_style/css/styler.css','leaflet_style/simple-color.css','leaflet_style/jquery.svg.css']
    return dict(css_files=css_files)
def get_icon_config(icon):
    iconUrl = static('markers/%s' % icon)
    if icon.startswith("marker"):
        return {
            'iconSize': [25, 41],
            'iconUrl': iconUrl,
            'iconAnchor': [12, 41],
            'shadowSize': [41, 41],
            'shadowUrl': static('markers/shadow.png')
        }
    elif icon.startswith("dot"):
        return {
            'iconSize': [17, 18],
            'iconUrl': iconUrl,
            'iconAnchor': [9, 9]
        }
    return {
        'iconSize': [17, 18],
        'iconUrl': iconUrl,
        'iconAnchor': [9, 9]
    }
def get_markers_list():
    markers_dir = os.path.join(settings.STATIC_ROOT, 'markers')

    return mark_safe(json.dumps([get_icon_config(f) for f in os.listdir(markers_dir) if os.path.isfile(os.path.join(markers_dir, f))]))

@register.inclusion_tag('leaflet_style/styler_js.html')
def leaflet_styler_js():
    js_files = [
        'leaflet_style/js/styler.js',
        'leaflet_style/jquery.simple-color.js',
        'leaflet_style/jquery.svg.min.js',
        #"leaflet_style/jquery.svgdom.min.js"
    ]
    return dict(js_files=js_files, markers_list=get_markers_list())

@register.inclusion_tag('leaflet_style/style_js.html')
def leaflet_style_js():
    js_files = ['leaflet_style/js/style.js']
    return dict(js_files=js_files)

@register.inclusion_tag('leaflet_style/styler.html')
def leaflet_styler(field_id, feature_type=None):
    return {
        "feature_type": feature_type,
        "field_id": field_id
    }