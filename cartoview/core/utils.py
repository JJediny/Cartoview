from subprocess import Popen
import os,sys
import urllib2
from django.contrib.auth.models import User,Group, Permission
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.gis.geos.polygon import Polygon
from cartoview2.core.models import *
from cartoview2.catalog import  models as catalog_models
from cartoview2 import settings

current_folder = os.path.dirname(__file__)
baselayers_urls = {
    'Streets':'http://services.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/export?bboxSR=4326&layers=&layerdefs=&size=300%2C200&imageSR=&format=png24&transparent=false&dpi=&time=&layerTimeOptions=&f=image&bbox=',
     "Gray": 'http://services.arcgisonline.com/arcgis/rest/services/Canvas/World_Light_Gray_Base/MapServer/export?bboxSR=4326&layers=&layerdefs=&size=300%2C200&imageSR=&format=png24&transparent=false&dpi=&time=&layerTimeOptions=&f=image&bbox=',
    "Google" :'http://maps.googleapis.com/maps/api/staticmap?zoom={zoom}&size=300x200&maptype=roadmap&center={center}',
    "Google Terrain" : 'http://maps.googleapis.com/maps/api/staticmap?zoom={zoom}&size=300x200&sensor=true_or_false&maptype=terrain&center={center}',
    "OSM" : '',
    "Topographic" : 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/export?bboxSR=4326&layers=&layerdefs=&size=300%2C200&imageSR=&format=png24&transparent=false&dpi=&time=&layerTimeOptions=&f=image&bbox='
}

def run_batch_file(path, params=None, cwd=current_folder):
    p = Popen(path)
    stdout, stderr = p.communicate()
    return stdout, stderr


def get_permitted (permission):
    try:
        group = Group.objects.get( permissions=permission)
        permitted_group = group
    except:
        permitted_group = None
    try :
        users = User.objects.filter( Q(user_permissions=permission) ).distinct()
        permitted_users = users
    except:
        permitted_users = None

    return permitted_users , permitted_group

decorator_with_arguments = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)

@decorator_with_arguments
def custom_permission_required(function, perm,redirect_url_name = 'cartoview2_permission_denied'):
    def _function(request, *args, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('account_login')+'?next='+request.path)
        if request.user.has_perm(perm):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(redirect_url_name))
            #request.user.message_set.create(message = "What are you doing here?!")
            # Return a response or redirect to referrer or some page of your choice
    return _function

@decorator_with_arguments
def superuser_required(function, redirect_url_name = 'cartoview2_permission_denied'):
    def _function(request, *args, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('account_login')+'?next='+request.path)
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(redirect_url_name))
            #request.user.message_set.create(message = "What are you doing here?!")
            # Return a response or redirect to referrer or some page of your choice
    return _function

def add_to_catalog (request , resource_form ,app_name , tags  ,extent):

    resource = resource_form.save(commit=False)
    resource.app = App.objects.get(name= app_name)
    resource.created_by = request.user
    resource.last_updated_by = request.user
    resource.save()
    resource.set_tags(tags)
    bbox = (extent[0], extent[1], extent[2], extent[3])
    resource.location_extent = Polygon.from_bbox(bbox)
    resource.save()
    resource_form.save_m2m()

    return resource
