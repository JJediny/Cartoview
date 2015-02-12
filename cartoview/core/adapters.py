from allauth.account.adapter import DefaultAccountAdapter
from cartoview2 import settings
class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):

        if 'next' in request.GET:
            return request.GET['next']
        else:
            if settings.SITE_ROOT :
                return '/'+settings.SITE_ROOT
            else:
                return '/'