import importlib

from django.conf.urls import patterns, include, url
from django.contrib import admin

from cartoview2.core.apps_helper import get_apps_names
from cartoview2.core.api import rest_api
from cartoview2 import settings


def import_app_rest(app_name):
    try:
        #print 'define %s rest api ....' % app_name
        module_ = importlib.import_module('apps.%s.rest' % app_name)
    except ImportError:
        pass

apps = get_apps_names()
for name in apps:
   import_app_rest(name)

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^', include('cartoview2.core.urls')),
    url(r'^catalog/', include('cartoview2.catalog.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #(r'^accounts/', include('registration.backends.default.urls')),
    (r'^rest/', include(rest_api.urls)),
    url(r'^accounts/', include('allauth.urls')),
)


#auto load apps urls
def app_url(app_name):
    app = str(app_name)
    return url(r'^' + app + '/', include('apps.%s.urls' % app), name=app + '_base_url')
for name in apps:
    urlpatterns.append(app_url(name))
    # try:
    #     print 'import %s urls' % name
    #     urlpatterns.append(app_url(name))
    #     print 'imported'
    # except Exception:
    #     pass

try:
    if settings.ROOT_URL and settings.ROOT_URL != '/' :
        urlpatterns = patterns('',url(r'^'+settings.ROOT_URL,include(urlpatterns)))
except :
    pass

def register_app_urls(app_name):
    urlpatterns.append(app_url(app_name))
    import_app_rest(app_name)
    rest_api.register_app_urls(app_name)
    from django.contrib import admin
    admin.autodiscover()

    print 'app urls registerd.'

