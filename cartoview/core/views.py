import urllib2
import httplib
from cartoview2 import get_version as get_carto_version
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from allauth.socialaccount.models import *
import json
from cartoview2.core.models import *
from cartoview2.core.forms import KeyValueForm , HomePageForm
from cartoview2.core.forms import SettingsForm as cartoview_settings_form
from cartoview2.core.cartoview_registeration.forms import SocialAppForm
from apps_helper import *
from django.conf import settings as django_settings
from django.db.models import Max, Min
from cartoview_registeration.models import Settings as registeration_settings
from cartoview_registeration.forms import SettingsForm as registeration_settings_form

from cartoview2.catalog.views import home as catalog_home
def home(request):
    context = {}
    home_keyvalue , created =KeyValue.objects.get_or_create(key='homepage')

    selected_home_name = home_keyvalue.value
    if ((selected_home_name=='catalog')or (selected_home_name==None)):
        return redirect(catalog_home)
    elif (selected_home_name=='featured'):
        return redirect(reverse(catalog_home)+'?filter=featured')
    else:
        return render(request,'cartoview2/'+selected_home_name +'.html',context)


def embed(request):
    embed_page =  request.GET.get('embed',None)
    if embed_page is not None:
        return {'embed_page': True}
    return {'embed_page': False}

def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)


def proxy(request, url):
    query_string = ''
    for k in request.GET:
        query_string += "%s=%s&" % (str(k) ,str(request.GET[k]))
    if query_string != '':
        url += '?' + query_string
    from datetime import datetime
    t = datetime.now()
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)

    try:
        status = response.getcode()
        response_body = response.read()
    except urllib2.HTTPError, e:
        response_body = e.read()
        status = e.code

    return HttpResponse(response_body, status=status, content_type=response.headers['content-type'])



@login_required
def settings(request):
    if (len(registeration_settings.objects.all()) > 0):
        reg_settings_obj = Site.objects.get_current().registeration_settings
    else:
        reg_settings_obj = None

    if (len(Settings.objects.all()) > 0):
        carto_settings_obj = Site.objects.get_current().cartoview_settings
    else:
        carto_settings_obj = None

    if request.method == 'POST':
        homepage_form = HomePageForm (request.POST, prefix='homepage_form')
        reg_settings_form = registeration_settings_form(request.POST,prefix='reg_settings_form',instance=reg_settings_obj)
        carto_settings_form = cartoview_settings_form(request.POST,prefix='carto_settings_form',instance=carto_settings_obj)
        if homepage_form.is_valid() and reg_settings_form.is_valid() and carto_settings_form.is_valid():
            homepage_form.save()
            #save registration settings
            reg_settings = reg_settings_form.save(commit=False)
            reg_settings.site = Site.objects.get_current()
            reg_settings.save()
            #save cartoview settings
            carto_settings = carto_settings_form.save(commit=False)
            carto_settings.site = Site.objects.get_current()
            carto_settings.save()
            return redirect(home)
        else :
            return redirect(catalog_home)
    else:
        context = {}



        reg_settings_form = registeration_settings_form(prefix='reg_settings_form', instance=reg_settings_obj)
        carto_settings_form = cartoview_settings_form(prefix='carto_settings_form',instance=carto_settings_obj)
        context["site_form"] = KeyValueForm(group_name='Site Settings')
        context["home_form"] = KeyValueForm(group_name='Home Page')
        home_keyvalue , created =KeyValue.objects.get_or_create(key='homepage')

        selected_home_name = home_keyvalue.value
        home_page_id = HomePage.objects.get(name=selected_home_name).pk
        context['homepage_form']=HomePageForm(prefix='homepage_form',initial={'homepage':home_page_id})
        fb_obj = SocialApp.objects.get(name="Facebook")
        twitter_obj = SocialApp.objects.get(name="Twitter")
        google_obj = SocialApp.objects.get(name="Google")
        linkedin_obj = SocialApp.objects.get(name="LinkedIn")
        context["fb_form"] = SocialAppForm(prefix="objects[0]",initial={"objects[0].id":fb_obj.id,"objects[0].client_id":fb_obj.client_id,"objects[0].secret":fb_obj.secret,"objects[0].provider":fb_obj.provider,"objects[0].name":fb_obj.name})
        context["twitter_form"] =SocialAppForm(prefix="objects[1]",initial={"objects[1].id":twitter_obj.id,"objects[1].client_id":twitter_obj.client_id,"objects[1].secret":twitter_obj.secret,"objects[1].provider":twitter_obj.provider,"objects[1].name":twitter_obj.name})
        context["google_form"] =SocialAppForm(prefix="objects[2]",initial={"objects[2].id":google_obj.id,"objects[2].client_id":google_obj.client_id,"objects[2].secret":google_obj.secret,"objects[2].provider":google_obj.provider,"objects[2].name":google_obj.name})
        context["linkedin_form"] = SocialAppForm(prefix="objects[3]",initial={"objects[3].id":linkedin_obj.id,"objects[3].client_id":linkedin_obj.client_id,"objects[3].secret":linkedin_obj.secret,"objects[3].provider":linkedin_obj.provider,"objects[3].name":linkedin_obj.name})

        apps = []
        for app in App.objects.all():
            try:
                config = importlib.import_module('apps.%s.config' % app.name)
                app_info = {
                    'name':app.name,
                    'title':app.title,
                }
                app_info['config_form'] = config.get_form()
                apps.append(app_info)
            except:
                pass
        menu_apps = App.objects.filter(is_suspended = False).filter(in_menu = True).order_by('order')
        non_menu_apps = App.objects.filter(is_suspended = False).filter(in_menu = False).order_by('order')
        context['menu_apps'] = menu_apps
        context['non_menu_apps'] = non_menu_apps
        context['apps'] = apps
        all_apps = App.objects.all().order_by('order')
        for app in all_apps:
            app.settings_url = get_url("%s_settings" % app.name)
        context['Apps'] = all_apps
        context['reg_settings_form'] = reg_settings_form
        context['carto_settings_form'] = carto_settings_form
        context['carto_version']= get_carto_version()
        return render(request,'cartoview2/settings.html',context)




def save_app_orders(request):
    if request.method == 'POST':
        apps_list = request.POST.get('apps', None)

        if apps_list:
            try:
                apps = json.loads(apps_list)
                menu_apps=apps['menu_apps']
                non_menu_apps=apps['non_menu_apps']
                for idx, val in enumerate(menu_apps):
                    app = App.objects.get(id = int(val['id']))
                    app.order = idx
                    app.in_menu = True
                    app.save()

                for idx, val in enumerate(non_menu_apps):
                    app = App.objects.get(id = int(val['id']))
                    app.order = idx + len(menu_apps)
                    app.in_menu = False
                    app.save()
                ajax_vars = {'success': True}
            except:
                ajax_vars = {'success': False}
                return HttpResponse(json.dumps(ajax_vars), content_type="application/json")



    return HttpResponse(json.dumps(ajax_vars), content_type="application/json")


current_folder, filename = os.path.split(os.path.abspath(__file__))
temp_dir = os.path.join(current_folder,'temp')


def save_uploaded_file(f,path):
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()



from apps_helper import install_app
from threading import Timer
from utils import run_batch_file
from django.core import management
def get_attr(obj,key,default):
    try:
      return obj[key]
    except:
        return default

def add_app(app_name, info):
    app = App()
    app.name = app_name
    app.title = get_attr(info,'title', app_name)
    app.description = get_attr(info, 'description', None)
    app.short_description = get_attr(info, 'short_description', None)
    app.owner_url = get_attr(info, 'owner_url', None)
    app.help_url = get_attr(info, 'help_url', None)
    BASE_DIR = getattr(django_settings, 'BASE_DIR', None)
    app_img_path = os.path.abspath(os.path.join(BASE_DIR,'apps',app_name,'app_img.png'))
    # img_temp = NamedTemporaryFile()
    #app_img_file = open(app_img_path)
    # img_temp.write(app_img_file.read())
    # img_temp.flush()
    # #app_img_file = File(open(app_img_path,'r'))
    if os.path.isfile(app_img_path):
        r = open(app_img_path,'rb')
        data = r.read()

        img_temp = NamedTemporaryFile()
        img_temp.write(data)
        img_temp.flush()
        app.app_img.save(app_name+'.png', File(img_temp))
    app_logo_path = os.path.abspath(os.path.join(BASE_DIR,'apps',app_name,'logo.png'))
    if os.path.isfile(app_logo_path):
        r_logo = open(app_logo_path,'rb')
        data_logo = r_logo.read()

        img_temp_logo = NamedTemporaryFile()
        img_temp_logo.write(data_logo)
        img_temp_logo.flush()
        app.app_logo.save(app_name+'_logo.png', File(img_temp_logo))
    app.author = get_attr(info, 'author', None)
    app.author_website = get_attr(info, 'author_website', None)
    app.home_page = get_attr(info, 'home_page', None)
    app.license = get_attr(info, 'licence', None)
    app.single_instance = get_attr(info, 'single_instance', False)
    apps = App.objects.all()
    if apps:
        app.order = apps.aggregate(Max('order'))['order__max']+1
    else:
        app.order = 1
    app.save()
    tags = get_attr(info,'tags',[])
    for tag_name in tags:
        try:
            tag = AppTag(name=tag_name)
            tag.save()
            app.tags.add(tag)
        except:
            pass
    management.call_command('syncdb', interactive=False)

def finalize_setup(app_name,user):
    def install():
        try:
            installer = importlib.import_module('apps.%s.installer' % app_name)
            add_app(app_name, installer.info)
            installer.install(user = user )
        except:
            pass

    restart_server_batch = getattr(django_settings, 'RESTART_SERVER_BAT', None)
    if restart_server_batch:
        def restart():
            install()
            run_batch_file(restart_server_batch, None, APPS_DIR)
        timer = Timer(0.1, restart)
        timer.start()
    else:
        try:
            install_app(app_name)
        except:
            pass
        install()

@login_required
def install_new_app(request):
    import tempfile
    import zipfile
    response_data = {
        'success': False,
        'log': [],
        'errors' : [],
        'warnings':[],
    }

    package_file = request.FILES.get('package_file',None)
    if package_file is None:
        response_data["errors"].append("No package file uploaded")
    else:
        response_data["log"].append("Package file uploaded")
        extract_to = tempfile.mkdtemp(dir=temp_dir)
        x, uploaded_file_path = tempfile.mkstemp(dir=temp_dir)
        save_uploaded_file(package_file,uploaded_file_path)
        # Get a real Python file handle on the uploaded file
        file_handle = open(uploaded_file_path, 'rb')
        # Unzip the file, creating subdirectories as needed
        zfobj = zipfile.ZipFile(file_handle)
        for name in zfobj.namelist():
            if name.startswith('__MACOSX/'):
                continue
            if name.endswith('/'):
                try: # Don't try to create a directory if exists
                    os.mkdir(os.path.join(extract_to, name))
                except:
                    pass
            else:
                outfile = open(os.path.join(extract_to, name), 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()
        response_data["log"].append("Package file extracted")
        app_name = os.listdir(extract_to)[0]
        no_installer = True
        response_data["app_name"] = app_name
        app_dir = os.path.join(extract_to, app_name)
        installed_app_dir = os.path.join(APPS_DIR, app_name)
        if os.path.isdir(installed_app_dir):
            response_data['warnings'].append('application %s is already exists' % app_name)
        else:
            shutil.move(app_dir, APPS_DIR)
            try:
                installer = importlib.import_module('apps.%s.installer' % app_name)
                no_installer = False
            except:
                pass
        response_data["success"] = True
        if no_installer:
            response_data['warnings'].append('no application installer found')
            
        os.close(x)
        zfobj.close()
        file_handle.close()
        os.remove(uploaded_file_path)

        shutil.rmtree(extract_to)
        finalize_setup(app_name,request.user)
        response_data["log"].append("Running installation scripts...")
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def uninstall_app(request, app_name):
    try:
        installer = importlib.import_module('apps.%s.installer' % app_name)
        installer.uninstall()
        app = App.objects.get(name=app_name)
        app.delete()
        response_data = {"success":True}
    except Exception as ex:
       response_data = {"success":False,"errors":[ex.message]}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def move_up(request, app_id):
    app = App.objects.get(id=app_id)
    prev_app = App.objects.get(order=App.objects.filter(order__lt=app.order).aggregate(Max('order'))['order__max'])
    order = app.order
    app.order = prev_app.order
    prev_app.order = order
    app.save()
    prev_app.save()
    return HttpResponse(json.dumps({"success":True}),content_type="application/json")

@login_required
def move_down(request, app_id):
    app = App.objects.get(id=app_id)
    next_app = App.objects.get(order=App.objects.filter(order__gt=app.order).aggregate(Min('order'))['order__min'])
    order = app.order
    app.order = next_app.order
    next_app.order = order
    app.save()
    next_app.save()
    return HttpResponse(json.dumps({"success":True}),content_type="application/json")


import sys
if sys.version < '3':
    text_type = unicode
else:
    text_type = str

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers



def urls_js(request):
    url_patterns = list(urlresolvers.get_resolver(None).reverse_dict.items())
    url_list = [(url_name, url_pattern[0][0]) for url_name, url_pattern in url_patterns if
                (isinstance(url_name, str) or isinstance(url_name, text_type))]

    return render_to_response('django_js_reverse/urls.js',{
          'urls': url_list,
          'url_prefix': urlresolvers.get_script_prefix()
      },
      context_instance=RequestContext(request), mimetype='application/javascript')

def permission_denied (request):
    return render(request,'cartoview2/permission_denied.html',{})

def suspend_app  (request,app_id):

    app = App.objects.get(id=app_id)
    app.is_suspended = True
    app.save()
    return HttpResponse(json.dumps({"success":True}),content_type="application/json")

def resume_app  (request,app_id):

    app = App.objects.get(id=app_id)
    app.is_suspended = False
    app.save()
    return HttpResponse(json.dumps({"success":True}),content_type="application/json")


def save_social_settings(request):
    if request.method == "POST":
        if (len(registeration_settings.objects.all()) > 0):
            settings_obj = Site.objects.get_current().registeration_settings
        else:
            settings_obj = None
        settings_form = registeration_settings_form(request.POST,prefix='settings_form',instance=settings_obj)
        settings = settings_form.save(commit=False)
        settings.site = Site.objects.get_current()
        settings.save()
        return HttpResponse(json.dumps({'message': 'done'}))

    return render_to_response('cartoview2/settings.html',
            {}, RequestContext(request))


def handler404(request):
    return render(request, 'cartoview2/404.html')

# def test (request):
#     context = {}
#     menu_apps = App.objects.filter(is_suspended = False).filter(in_menu = True).order_by('order')
#     non_menu_apps = App.objects.filter(is_suspended = False).filter(in_menu = False).order_by('order')
#     context['menu_apps'] = menu_apps
#     context['non_menu_apps'] = non_menu_apps
#
#     return render_to_response('cartoview2/test.html',
#             context, RequestContext(request))
