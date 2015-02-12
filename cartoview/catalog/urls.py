import os

from django.conf.urls import patterns, url , include


urlpatterns = patterns('',
    url(r'^$', 'cartoview2.catalog.views.home', name='catalog_base_url'),
    (r'^results/$', 'cartoview2.catalog.views.results'),
    (r'^tag/(?P<tag_id>\d+)/$', 'cartoview2.catalog.views.tag_results'),
    url (r'^resources/user/(?P<user_id>\d+)/$', 'cartoview2.catalog.views.user_results' , name = 'user_resources'),
    (r'^category/(?P<category_id>\d+)/$', 'cartoview2.catalog.views.category_results'),
    (r'^search/$', 'cartoview2.catalog.views.search_results'),
    url(r'^resource/(?P<resource_id>\d+)/$', 'cartoview2.catalog.views.resource_details', name='resource_details'),
    (r'^resource/delete/(?P<resource_id>\d+)/$', 'cartoview2.catalog.views.resource_delete'),
    (r'^resource/edit/(?P<resource_id>\d+)/$', 'cartoview2.catalog.views.resource_edit'),
    (r'^resource/(?P<resource_id>\d+)/(?P<slug>[-\w]+)/$', 'cartoview2.catalog.views.resource_details'),
    (r'^tags/$', 'cartoview2.catalog.views.get_tag_list'),
    (r'^apps/$', 'cartoview2.catalog.views.get_app_list'),
    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^csw_catalog/', include('cartoview2.catalog.csw_catalog.urls')),
    url(r'^submit/', 'cartoview2.catalog.views.submit',name='catalog_submit'),
    url(r'^submit_api/(?P<resource_id>\d+)/$','cartoview2.catalog.views.API_submit', name='catalog.submit_api'),
    url(r'^submit_data/(?P<resource_id>\d+)/$','cartoview2.catalog.views.Data_submit', name='catalog.submit_data'),
    url(r'^submit_app/(?P<resource_id>\d+)/$','cartoview2.catalog.views.App_submit', name='catalog.submit_app'),
    url(r'^settings/', 'cartoview2.catalog.views.settings',name = 'catalog_settings'),
    url(r'^new/', 'cartoview2.catalog.views.create_new', name='create_new'),
    url(r'^validate_url/', 'cartoview2.catalog.views.validate_url', name='validate_url'),
    url(r'^security/permissions/(?P<resource_id>\d+)$',
                           'cartoview2.catalog.security.views.resource_permissions',
                           name='resource_permissions'),
    url(r'^account/ajax_lookup$', 'cartoview2.catalog.security.views.ajax_lookup',
                           name='account_ajax_lookup'),

)

import rest