# Django settings for cartoview2 project.
import os,sys
current_folder = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_folder, os.path.pardir, 'apps')))

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'viw&se#qdtf*3lgxd2v5elbmlvj4ok4equc8fgx&ak(tb_9ah='

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
# ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'core', 'templates', 'cartoview2'),
)
COMMENTS_APP = 'cartoview2.catalog.comments'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.flatpages',
    'django.contrib.comments',
    #'registration',
    #cartoview2 core
    'cartoview2.core',
    'cartoview2.core.cartoview_registeration',
    'cartoview2.catalog',
    'cartoview2.catalog.comments',
    'cartoview2.catalog.csw_catalog',
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
    'tastypie',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'form_utils',
    'sorl.thumbnail',
	##For open data catalog
    'django_sorting',
    'djangoratings',
	'pagination',
    #'debug_toolbar',
    'leaflet',
	'disqus',
	'guardian',
    'cartoview2.catalog.security',
	'cartoview2.core.forms_custom',
)
DISQUS_API_KEY = 'ywgGNbC33vpYOhaw4adwIUr8I8puw1k7ZjTF3h3uDHASpVriyc3QBYfE9mSw6Uux'
DISQUS_WEBSITE_SHORTNAME = 'cartoview'



# added by kamal on 26/1/2014
# this is to use the request object in template code like {{ request.get_full_path }} or {{ request.path }}
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    "django.contrib.auth.context_processors.auth",
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    "cartoview2.core.configuration.configuration",
    "cartoview2.core.apps_helper.installed_apps",
    "cartoview2.core.views.embed",
	"cartoview2.catalog.context_processors.get_current_path",
    "cartoview2.catalog.context_processors.get_settings",

)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
	'guardian.backends.ObjectPermissionBackend',
)
ALLOWED_HOSTS = ['.cartoview.cartologic.com','.cartoview.cartologic.com.']
TIME_ZONE = 'GMT'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.abspath(os.path.join(current_folder, os.path.pardir, 'cartoview2', 'core', 'media'))
MEDIA_URL = '/media/'

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
	##For open data catalog
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django_sorting.middleware.SortingMiddleware',
    'pagination.middleware.PaginationMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cartoview2.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'cartoview2.wsgi.application'

ADAPTER = "cartoview2.core.adapters.MyAccountAdapter"
ACCOUNT_ADAPTER = "cartoview2.core.adapters.MyAccountAdapter"

#LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'oauth2'  # instead of 'oauth2'
    },

    'twitter': {
        'SCOPE': ['email'],
    },
}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
from deploy_settings import *

#auto load apps
from cartoview2.core.apps_helper import get_apps_names, APPS_DIR

CARTOVIEW2_APPS = ()

import importlib, sys

for app_name in get_apps_names():
    try:
        CARTOVIEW2_APPS += ('apps.' + app_name,)
        #settings_module = importlib.import_module('apps.%s.settings' % app_name)
        app_settings_file = os.path.join(APPS_DIR, app_name, 'settings.py')
        if os.path.exists(app_settings_file):
            # By doing this instead of import, app/settings.py can refer to
            # local variables from settings.py without circular imports.
            execfile(app_settings_file)
            # CARTOVIEW2_APPS += settings_module.apps
            # this_module = sys.modules[__name__]
            # GLOBAL_SETTINGS = getattr(settings_module,'GLOBAL_SETTINGS',{})
            # for key in GLOBAL_SETTINGS:
            #     current_val = getattr(this_module,key,None)
            #     if current_val is None:
            #         setattr(this_module, key, GLOBAL_SETTINGS[key])
            #     else:
            #         print '==========================='
            #         print 'warning: app %s trying to set the settings item "%s" which already has a value.' % (app_name,key)
    except:
        pass

INSTALLED_APPS += CARTOVIEW2_APPS

ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'cartoview.cartologic@gmail.com'
EMAIL_HOST_PASSWORD = 'clogic0706'
EMAIL_PORT = 587

ANONYMOUS_USER_ID = -1
