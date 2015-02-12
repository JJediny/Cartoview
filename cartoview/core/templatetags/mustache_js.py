__author__ = 'kamal'

import os
from django import template
from django.utils.safestring import mark_safe
register = template.Library()
from importlib import import_module

def get_app_dir(app):
    module = import_module(app)
    return os.path.dirname(module.__file__)

#TODO convert this to template tag not filter
@register.filter
def load_mustache_template(filename, app, script_id=None):
    script_id = script_id or filename.replace(".", "_")
    app_dir = get_app_dir(app)
    mustache_template_folder = os.path.join(app_dir,  'mustache_templates')
    filepath = os.path.join(mustache_template_folder, filename)
    with open(filepath, "r") as fp:
        template_text = fp.read()
    return mark_safe('<script id="%s" type="x-tmpl-mustache" >%s</script>' % (script_id, template_text))


register.simple_tag(load_mustache_template)
