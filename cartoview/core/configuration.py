from django.contrib.sites.models import Site
from cartoview2.core.models import KeyValueGroup

#TODO store in cache
def configuration(request):
    try:
        reg_settings_obj = Site.objects.get_current().registeration_settings
    except:
        reg_settings_obj = None
    try:
        carto_settings_obj = Site.objects.get_current().cartoview_settings
    except:
        carto_settings_obj = None

    obj = {'social_registration_settings': reg_settings_obj ,
           'carto_settings':carto_settings_obj,
        }
    for group in KeyValueGroup.objects.all():
        for item in group.keyvalue_set.all():
            key = group.name + "_" + item.key
            obj[key.replace(' ','_').lower()] = item.value
    return obj
