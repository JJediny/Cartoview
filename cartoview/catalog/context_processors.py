from django.conf import settings
from models import Settings
from django.contrib.sites.models import Site
def get_current_path(request):
    return {'current_path': request.get_full_path()}

def get_settings(request):

    if (len(Settings.objects.all()) > 0):
        settings_obj = Site.objects.get_current().catalog_settings
    else:
        settings_obj = Settings(title = 'Gallery' , enable_rating = True , site = Site.objects.get_current() )


    return {'settings':settings_obj,'SITE_ROOT':settings.SITE_ROOT}