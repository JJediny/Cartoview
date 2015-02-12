import importlib
import zipfile
import shutil

from tastypie import fields
from django.contrib.gis.geos.polygon import Polygon
from tastypie.constants import ALL
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.contrib.auth.forms import UserCreationForm
from cartoview2.core.resources import BaseModelResource , FileUploadResource
from cartoview2.core.models import *
from cartoview2.core.models import temp_dir
from cartoview2.core.apps_helper import APPS_DIR


class UserResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        can_edit = True
    def get_form(self, obj=None):
        return UserCreationForm(instance=obj)

    '''
    def prepend_urls(self):

        return [
            url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]
    '''
    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.raw_post_data, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)


class AppResource(FileUploadResource):
    class Meta(FileUploadResource.Meta):
        queryset = App.objects.all()
        filtering = {"name": ALL }
        can_edit = True


class AppInstanceResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = AppInstance.objects.all()
        filtering = {"id": ALL }
        can_edit = True

    owner = fields.ForeignKey(UserResource, 'owner', full=True)
    app = fields.ForeignKey(AppResource, 'app', full=True)
    can_edit = fields.BooleanField(default=False)
    location_extent = fields.ListField()

    def dehydrate_can_edit(self, bundle):
        return bundle.obj.owner == bundle.request.user

    def dehydrate_location_extent(self, bundle):
        if bundle.obj.location_extent:
            return bundle.obj.location_extent.extent
        return None

    def hydrate_location_extent(self, bundle):
        if 'location_extent' in bundle.data:
            e = bundle.data['location_extent']
            bbox = (e[0],e[1],e[2],e[3])
            bundle.obj.location_extent = Polygon.from_bbox(bbox)
        return bundle


class KeyValueResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = KeyValue.objects.all()
        can_edit = True


class KeyValueGroupResource(BaseModelResource):
    values = fields.ToManyField(KeyValueResource, 'keyvalue_set', full=True, null = True)

    class Meta(BaseModelResource.Meta):
        queryset = KeyValueGroup.objects.all()
        can_edit = True




from cartoview2.core.api import rest_api

rest_api.register(AppResource())
rest_api.register(UserResource())
rest_api.register(AppInstanceResource())
rest_api.register(KeyValueResource())
rest_api.register(KeyValueGroupResource())
