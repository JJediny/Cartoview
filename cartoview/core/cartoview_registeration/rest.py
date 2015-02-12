from allauth.socialaccount.models import *

from cartoview2.core.resources import BaseModelResource
from cartoview2.core.serializers import HTMLSerializer
from cartoview2.core.api import rest_api
from tastypie import fields

class SocialAppResource(BaseModelResource):
    #enable_social = fields.BooleanField()
    class Meta(BaseModelResource.Meta):
        queryset = SocialApp.objects.all()
        serializer = HTMLSerializer()
        resource_name = 'socialapp'

    def hydrate_provider(self, bundle):
        social_app = self.Meta.queryset.get(pk=bundle.data['id'])
        bundle.obj.provider = social_app.provider
        return bundle

    def hydrate_name(self, bundle):
        social_app = self.Meta.queryset.get(pk=bundle.data['id'])
        bundle.obj.name = social_app.name
        return bundle

    def hydrate_key(self, bundle):
        social_app = self.Meta.queryset.get(pk=bundle.data['id'])
        bundle.obj.key = social_app.key
        return bundle


rest_api.register(SocialAppResource())
