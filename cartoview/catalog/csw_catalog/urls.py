from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^csw$','cartoview2.catalog.csw_catalog.views.csw'),
)
