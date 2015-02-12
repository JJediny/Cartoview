from guardian.shortcuts import get_objects_for_user
from tastypie import fields
from django.contrib.gis.geos.polygon import Polygon
from tastypie.constants import ALL,ALL_WITH_RELATIONS
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden

from cartoview2.core.rest import *
from cartoview2.catalog.models import *

from cartoview2.core.resources import BaseModelResource

class TagResource(BaseModelResource):


    class Meta(BaseModelResource.Meta):
        queryset = Tag.objects.all()
        can_edit = True

    def dehydrate(self, bundle):
        anonymous_user = get_user_model().objects.get(username='AnonymousUser')
        resources_with_view_permission = get_objects_for_user(bundle.request.user, 'catalog.view_resource')\
                                         | get_objects_for_user(anonymous_user, 'catalog.view_resource')
        tag_res_with_view_perm = (bundle.obj.resource_set.all() & resources_with_view_permission)
        bundle.data['resource_count'] = tag_res_with_view_perm.count()
        return bundle
class CategoryResource(BaseModelResource):


    class Meta(BaseModelResource.Meta):
        queryset = Category.objects.all()
        can_edit = True

    def dehydrate(self, bundle):
        anonymous_user = get_user_model().objects.get(username='AnonymousUser')
        resources_with_view_permission = get_objects_for_user(bundle.request.user, 'catalog.view_resource')\
                                         | get_objects_for_user(anonymous_user, 'catalog.view_resource')
        category_res_with_view_perm = (bundle.obj.resource_set.all() & resources_with_view_permission)
        bundle.data['resource_count'] = category_res_with_view_perm.count()
        return bundle
class DataTypeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = DataType.objects.all()
        can_edit = True

class UrlTypeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = UrlType.objects.all()
        can_edit = True
        filtering = {"url_type": ALL}



class UpdateFrequencyResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = UpdateFrequency.objects.all()
        can_edit = True

class CoordSystemResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = CoordSystem.objects.all()
        can_edit = True


class UrlImageResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = UrlImage.objects.all()
        can_edit = True

class ProviderResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Provider.objects.all()
        can_edit = True
        filtering = { "provider": ALL ,
                      "id":ALL }

class ServiceTypeResource(BaseModelResource):
    provider = fields.ForeignKey(ProviderResource, 'provider', full=True, null = True)
    class Meta(BaseModelResource.Meta):
        queryset = ServiceType.objects.all()
        can_edit = True
        filtering = {
            'provider': ALL_WITH_RELATIONS,
            'service_type': ALL
        }

class UrlResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Url.objects.all()
        can_edit = True
        filtering = {
            "url_type": ALL_WITH_RELATIONS,
            "service_type": ALL_WITH_RELATIONS
        }

    url_type = fields.ForeignKey(UrlTypeResource, 'url_type', full=True, null = True)
    url_images = fields.ToManyField(UrlImageResource, 'urlimage_set', full=True, null = True)
    service_type = fields.ForeignKey(ServiceTypeResource, 'service_type', full=True, null = True)



class CatalogResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Resource.objects.all()
        can_edit = True
        resource_name = 'resource'

    update_frequency = fields.ForeignKey(UpdateFrequency,'updates',full=True, null = True)
    created_by = fields.ForeignKey(UserResource, 'created_by', full=True, null = True)
    last_updated_by = fields.ForeignKey(UserResource, 'last_updated_by', full=True, null = True)
    urls = fields.ToManyField(UrlResource, 'url_set', full=True, null = True)

from cartoview2.core.api import rest_api

rest_api.register(TagResource())
rest_api.register(CategoryResource())

rest_api.register(DataTypeResource())
rest_api.register(UrlTypeResource())
rest_api.register(UpdateFrequencyResource())
rest_api.register(CoordSystemResource())
rest_api.register(UrlResource())
rest_api.register(UrlImageResource())
rest_api.register(CatalogResource())
rest_api.register(ProviderResource())
rest_api.register(ServiceTypeResource())