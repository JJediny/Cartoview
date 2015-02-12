import importlib, os, sys, shutil
current_folder, filename = os.path.split(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(current_folder,os.path.pardir,os.path.pardir)
APPS_DIR = os.path.join(PROJECT_ROOT,'apps')
APPS_DIR = os.path.abspath(APPS_DIR)
INSTALLED_APPS_FILE = os.path.join(PROJECT_ROOT,'installed_apps.txt')


def get_apps_names():
    return [n for n in os.listdir(APPS_DIR) if os.path.isdir(os.path.join(APPS_DIR, n)) and n != '.svn' ]


def delete_installed_app(app):
    app_path = os.path.join(APPS_DIR, app.name)
    shutil.rmtree(app_path)

def install_app(app_name):
    from django.conf import settings
    settings.INSTALLED_APPS.append ('apps.%s' % app_name)
    from django.db.models.loading import load_app
    load_app('apps.%s' % app_name)
    from django.core.management import call_command
    call_command('syncdb',load_initial_data=False)
    try:
        print os.path.join(APPS_DIR,app_name,'fixtures')
        call_command('loaddata', os.path.join(APPS_DIR,app_name,'fixtures','initial_data.json'))
    except Exception:
        pass
    from cartoview2.urls import register_app_urls
    register_app_urls(app_name)

def get_url(url_name):
    from django.core.urlresolvers import reverse
    try:
        return reverse(url_name)
    except:
        return None

def installed_apps(request):
    from models import App
    apps = App.objects.filter(is_suspended = False).order_by('order')

    for app in apps:
        app.settings_url = get_url("%s_settings" % app.name)
        app.new_url = get_url(("%s.new" % app.name))

    return {"CARTOVIEW_APPS":apps}