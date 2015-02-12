import os

from django.conf.urls import patterns, url, include
from django.conf import settings
import views
current_folder, filename = os.path.split(os.path.abspath(__file__))
from cartoview2.core.proxy.views import proxy_view
urlpatterns = patterns('',
    url(r'^settings/$', views.settings, name='cartoview2_settings_url'),
     # url(r'^test/$', views.test, name='core_test'),
    url(r'^permission_denied/$',views.permission_denied , name='cartoview2_permission_denied'),
    url(r'^apps/install/$', views.install_new_app, name='cartoview2_install_app_url'),
    url(r'^apps/uninstall/(?P<app_name>.*)/$', views.uninstall_app, name='cartoview2_uninstall_app_url'),
    url(r'^apps/moveup/(?P<app_id>\d+)/$', views.move_up, name='move_up'),
    url(r'^apps/movedown/(?P<app_id>\d+)/$', views.move_down, name='move_down'),
    url(r'^apps/suspend/(?P<app_id>\d+)/$', views.suspend_app, name='suspend'),
    url(r'^apps/resume/(?P<app_id>\d+)/$', views.resume_app, name='resume'),
    url(r'^proxy/(?P<url>.*)$', proxy_view, name='cartoview2_proxy_url'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name='media'),
    url(r'^django_urls.js', 'cartoview2.core.views.urls_js', name='js_reverse'), #TODO: check if this is a security issue
    url(r'^$', views.home, name='cartoview2_base_url'),
     url(r'^save_social_settings/$', 'cartoview2.core.views.save_social_settings', name='save_social_settings'),
     url(r'^save_app_orders/$', 'cartoview2.core.views.save_app_orders', name='save_app_orders'),
     url(r'^forms_custom/', include('cartoview2.core.forms_custom.urls', namespace='forms_custom')),


)

import rest
from cartoview2.core.cartoview_registeration import rest