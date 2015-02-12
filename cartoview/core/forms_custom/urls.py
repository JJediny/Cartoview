# coding=utf-8

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('base.fields.views',
                       url(r'^tree_widget/(?P<application>\w+)/(?P<model_name>\w+)/$', 
                           view=views.tree_widget, name='tree_widget'),
                       url(r'^autocomplete_widget/(?P<application>\w+)/(?P<model_name>\w+)/$', 
                           view=views.autocomplete_widget, name='autocomplete_widget'),
                       )
