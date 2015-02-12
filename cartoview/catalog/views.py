import random

from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.core import serializers
from django.core.mail import send_mail, mail_managers, EmailMessage
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import get_objects_for_user, get_objects_for_group
import pytz
from pytz import timezone
from django.core.cache import cache
from cartoview2.core.forms import permissions_formset
from cartoview2.core.utils import custom_permission_required, superuser_required
from models import TwitterCache
import twitter
import simplejson as json
from cartoview2.core import models as core_models
from models import *
from forms import *
from django.core.urlresolvers import reverse


def get_tags_json():
    tag_objects = Tag.objects.all()
    if tag_objects:
        tag_names = []
        for t in tag_objects:
            tag_names.append(t.tag_name)
        return json.dumps(tag_names)
    else:
        return None

###########################################
def home(request):
    tweets = cache.get('tweets')

    utc = pytz.utc
    local = timezone('US/Eastern')

    """if not tweets and settings.TWITTER_USER:
        tweets = twitter.Api().GetUserTimeline( settings.TWITTER_USER )[:4]
        if tweets.count < 4:
            tweet_cache = []
            for t in TwitterCache.objects.all():
                tc = json.JSONDecoder().decode(t.text)
                tc['date'] = datetime.strptime( tc['created_at'], "%a %b %d %H:%M:%S +0000 %Y" ).replace(tzinfo=utc).astimezone(local)
                tweet_cache.append(tc)
            tweets = tweet_cache
        else:
            TwitterCache.objects.all().delete()
            for tweet in tweets:
                tweet.date = datetime.strptime( tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y" ).replace(tzinfo=utc).astimezone(local)
                t = TwitterCache(text=tweet.AsJsonString())
                t.save()
            cache.set( 'tweets', tweets, settings.TWITTER_TIMEOUT )"""

    #recent = Resource.objects.order_by("-created")[:3]
    anonymous_user = get_user_model().objects.get(username='AnonymousUser')
    anonymous_group, created = Group.objects.get_or_create(name='anonymous')
    resources_with_view_permission = get_objects_for_user(request.user, 'catalog.view_resource')\
                                     | get_objects_for_user(anonymous_user, 'catalog.view_resource')
    recent = resources_with_view_permission.order_by("-is_featured", "-created").filter(Q(app__is_suspended=False) | Q(app=None))
    if (len(Settings.objects.all()) > 0):
        settings_obj = Site.objects.get_current().catalog_settings
    else:
        settings_obj = Settings(title = 'Gallery' , enable_rating = True , site = Site.objects.get_current() )

    if( (settings_obj.default_view == 'featured') and (not ('filter' in request.GET)) ):
        featured_url = reverse('catalog_base_url')+'?filter=featured'
        return HttpResponseRedirect(featured_url)


    if 'filter' in request.GET:
        f = request.GET['filter']
        if f == 'featured':
            recent = recent.filter(is_featured=True)
        elif f == "my_maps":
            recent = recent.filter(created_by=request.user)
        else:
            recent = recent.filter(url__url_type__url_type__iexact=f).distinct()
        #idea = Idea.objects.order_by("-created_by_date")[:4]
    return render_to_response('catalog/home.html', {'recent': recent, 'tweets': tweets},
                              context_instance=RequestContext(request))

#####################################################################################
@custom_permission_required('catalog.delete_resource')
def resource_delete(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    resource_tags = resource.tags.all()
    for tag in resource_tags:
        if tag.resource_set.count() == 1:
            tag.delete()
    resource.delete()
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    # if 'HTTP_REFERER' in request.META:
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(home)


def results(request):
    anonymous_user = get_user_model().objects.get(username='AnonymousUser')
    resources_with_view_permission = get_objects_for_user(request.user, 'catalog.view_resource')\
                                     | get_objects_for_user(anonymous_user, 'catalog.view_resource')
    resources = resources_with_view_permission.order_by("-is_featured", "-created").filter(Q(app__is_suspended=False) | Q(app=None))
    if 'filter' in request.GET:
        f = request.GET['filter']
        if f == 'featured':
            resources = resources.filter(is_featured=True)
        else:
            resources = resources.filter(url__url_type__url_type__iexact=f).distinct()
    return render_to_response('catalog/results.html', {'results': resources}, context_instance=RequestContext(request))

#####################################################33
def invalid_submit(request, submission_form, url_form, urlimage_form, api_form, data_form):
    context = {'submission_form': submission_form, 'url_form': url_form, 'urlimage_form': urlimage_form,
               'api_form': api_form, 'data_form': data_form}

    return render_to_response('catalog/submit.html', context, context_instance=RequestContext(request))

####################################################################
def save_resource(request, submission_form, url_form, urlimage_form, api_form, data_form):
    if submission_form.is_valid() and url_form.is_valid() and urlimage_form.is_valid():
        resource = submission_form.save(commit=False)
        resource.created_by = request.user
        resource.last_updated_by = request.user
        tags = request.POST.get('appInstance_form-tags')
        tags = tags.split(',')
        resource.save()
        submission_form.save_m2m()
        resource.set_tags(tags)
        url = url_form.save(commit=False)
        url.resource = resource
        url.save()
        url_image = urlimage_form.save(commit=False)
        if (url_image.image):
            url_image.url = url
            url_image.save()
        resource.csw_xml = resource.gen_csw_xml()
        resource.save()
        if (url.url_type.url_type == 'API'):
            if (api_form.is_valid()):
                api = api_form.save(commit=False)
                url.service_type = api.service_type
                url.provider = api.provider
                url.save()
            else:
                context = {'submission_form': submission_form, 'url_form': url_form, 'urlimage_form': urlimage_form,
                           'api_form': api_form, 'data_form': data_form}

                return render_to_response('catalog/submit.html', context, context_instance=RequestContext(request))

        if ((url.url_type.url_type == 'Data')):
            if (data_form.is_valid()):
                data = data_form.save(commit=False)
                for data_type in data_form.cleaned_data['data_types']:
                    resource.data_types.add(data_type)
                resource.csw_xml = resource.gen_csw_xml()
                resource.save()
            else:
                context = {'submission_form': submission_form, 'url_form': url_form, 'urlimage_form': urlimage_form,
                           'api_form': api_form, 'data_form': data_form}

                return render_to_response('catalog/submit.html', context, context_instance=RequestContext(request))
        return render_to_response('catalog/success.html', {}, context_instance=RequestContext(request))
    else:
        context = {'submission_form': submission_form, 'url_form': url_form, 'urlimage_form': urlimage_form,
                   'api_form': api_form, 'data_form': data_form}

        return render_to_response('catalog/submit.html', context, context_instance=RequestContext(request))


##########################################################################################################################
def save_API(request, resource_obj, url_form, urlimage_form):
    if url_form.is_valid() and urlimage_form.is_valid():
        resource = resource_obj
        url = url_form.save(commit=False)
        url.save()
        url_image = urlimage_form.save(commit=False)
        if (url_image.image):
            url_image.url = url
            url_image.save()
        resource.csw_xml = resource.gen_csw_xml()
        resource.save()
        return render_to_response('catalog/success.html', {}, context_instance=RequestContext(request))
    else:
        context = {'url_form': url_form, 'urlimage_form': urlimage_form}
        return render_to_response('catalog/submit_api.html', context, context_instance=RequestContext(request))

#########################################################################################################
def save_Data(request, resource_obj, url_obj, data_form, urlimage_form):
    if data_form.is_valid() and urlimage_form.is_valid():
        resource = resource_obj
        res_data = data_form.save()
        url_image = urlimage_form.save(commit=False)
        if (url_image.image):
            url_image.url = url_obj
            url_image.save()
        resource.csw_xml = resource.gen_csw_xml()
        resource.save()
        return render_to_response('catalog/success.html', {}, context_instance=RequestContext(request))
    else:
        context = {'data_form': data_form, 'urlimage_form': urlimage_form}
        return render_to_response('catalog/submit_data.html', context, context_instance=RequestContext(request))

##########################################################################################################
def save_App(request, resource_obj, url_obj, urlimage_form):
    if urlimage_form.is_valid():
        resource = resource_obj
        url_image = urlimage_form.save(commit=False)
        url_image.url = url_obj
        if (url_image.image):
            url_image.url = url_obj
            url_image.save()
        resource.csw_xml = resource.gen_csw_xml()
        resource.save()
        return render_to_response('catalog/success.html', {}, context_instance=RequestContext(request))
    else:
        context = {'urlimage_form': urlimage_form}
        return render_to_response('catalog/submit_app.html', context, context_instance=RequestContext(request))

#############################################################################################################
@custom_permission_required('catalog.add_resource')
def submit(request):
    if request.method == 'POST':
        submission_form = SubmissionForm(request.POST, prefix='submission_form')
        url_form = UrlForm(request.POST, prefix='url_form')
        urlimage_form = UrlImageForm(request.POST, prefix='urlimage_form', files=request.FILES)
        api_form = APIform(request.POST, prefix='api_form')
        data_form = DataTypeForm(request.POST, prefix='data_form')

        return save_resource(request, submission_form, url_form, urlimage_form, api_form, data_form)
    else:
        context = {
            'submission_form': SubmissionForm(prefix='submission_form'),
            'url_form': UrlForm(prefix='url_form'),
            'urlimage_form': UrlImageForm(prefix='urlimage_form'),
            'api_form': APIform(prefix='api_form'),
            'data_form': DataTypeForm(prefix='data_form'),
            'all_tags': get_tags_json()
        }
    return render_to_response('catalog/submit.html', context, context_instance=RequestContext(request))

###########################################################################################
def API_submit(request, resource_id):
    resource_obj = Resource.objects.get(id=resource_id)
    url_obj = Url.objects.get(resource_id=resource_id)
    try:
        url_img = UrlImage.objects.get(url_id=url_obj.pk)
    except:
        url_img = None

    if request.method == 'POST':
        url_form = APIform(request.POST, prefix='url_form', instance=url_obj)
        urlimage_form = UrlImageForm(request.POST, prefix='urlimage_form', files=request.FILES, instance=url_img)
        return save_API(request, resource_obj, url_form, urlimage_form)
    else:
        context = {
            'url_form': APIform(prefix='url_form', instance=url_obj),
            'urlimage_form': UrlImageForm(prefix='urlimage_form', files=request.FILES, instance=url_img),
        }
    return render(request, 'catalog/submit_api.html', context)

#####################################################################################################
###########################################################################################
def Data_submit(request, resource_id):
    resource_obj = Resource.objects.get(id=resource_id)
    url_obj = Url.objects.get(resource_id=resource_id)
    try:
        url_img = UrlImage.objects.get(url_id=url_obj.pk)
    except:
        url_img = None

    if request.method == 'POST':
        data_form = DataTypeForm(request.POST, prefix='data_form', instance=resource_obj)
        urlimage_form = UrlImageForm(request.POST, prefix='urlimage_form', files=request.FILES, instance=url_img)
        return save_Data(request, resource_obj, url_obj, data_form, urlimage_form)
    else:
        context = {
            'data_form': DataTypeForm(prefix='data_form', instance=resource_obj),
            'urlimage_form': UrlImageForm(prefix='urlimage_form', files=request.FILES, instance=url_img),
        }
    return render(request, 'catalog/submit_data.html', context)

#####################################################################################################
###########################################################################################
def App_submit(request, resource_id):
    resource_obj = Resource.objects.get(id=resource_id)
    url_obj = Url.objects.get(resource_id=resource_id)
    try:
        url_img = UrlImage.objects.get(url_id=url_obj.pk)
    except:
        url_img = None

    if request.method == 'POST':
        urlimage_form = UrlImageForm(request.POST, prefix='urlimage_form', files=request.FILES, instance=url_img)
        return save_App(request, resource_obj, url_obj, urlimage_form)
    else:
        context = {
            'urlimage_form': UrlImageForm(prefix='urlimage_form', files=request.FILES, instance=url_img),
        }
    return render(request, 'catalog/submit_app.html', context)

#####################################################################################################
@custom_permission_required('catalog.change_resource')
def resource_edit(request, resource_id):
    res_obj = Resource.objects.get(pk=resource_id)
    url_obj = res_obj.url_set.all()[0]
    urlimage_obj = None
    if (len(url_obj.urlimage_set.all()) > 0):
        urlimage_obj = url_obj.urlimage_set.all()[0]
    if request.method == 'POST':
        submission_form = SubmissionForm(request.POST, prefix='submission_form', instance=res_obj)
        url_form = UrlForm(request.POST, prefix='url_form', instance=url_obj)
        urlimage_form = UrlImageForm(request.POST, prefix='urlimage_form', instance=urlimage_obj, files=request.FILES)
        api_form = APIform(request.POST, prefix='api_form', instance=url_obj)
        data_form = DataTypeForm(request.POST, prefix='data_form', instance=res_obj)
        return save_resource(request, submission_form, url_form, urlimage_form, api_form, data_form)
    else:
        context = {
            'submission_form': SubmissionForm(prefix='submission_form', instance=res_obj),
            'url_form': UrlForm(prefix='url_form', instance=url_obj),
            'urlimage_form': UrlImageForm(prefix='urlimage_form', instance=urlimage_obj, files=request.FILES),
            'api_form': APIform(prefix='api_form', instance=url_obj),
            'data_form': DataTypeForm(prefix='data_form', instance=res_obj),
            'all_tags': get_tags_json(),
            'tags': res_obj.get_tags()}
    return render_to_response('catalog/submit.html', context, context_instance=RequestContext(request))


def thanks(request):
    return render_to_response('catalog/thanks.html', context_instance=RequestContext(request))


def tag_results(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    anonymous_user = get_user_model().objects.get(username='AnonymousUser')
    resources_with_view_permission = get_objects_for_user(request.user, 'catalog.view_resource')\
                                     | get_objects_for_user(anonymous_user, 'catalog.view_resource')

    tag_resources = resources_with_view_permission.filter(tags=tag)
    if 'filter' in request.GET:
        f = request.GET['filter']
        tag_resources = tag_resources.filter(url__url_type__url_type__icontains=f).distinct()

    return render_to_response('catalog/results.html', {'results': tag_resources, 'tag': tag},
                              context_instance=RequestContext(request))

def user_results(request, user_id):
    user = get_user_model().objects.get(pk=user_id)
    anonymous_user = get_user_model().objects.get(username='AnonymousUser')
    resources_with_view_permission = get_objects_for_user(request.user, 'catalog.view_resource')\
                                     | get_objects_for_user(anonymous_user, 'catalog.view_resource')

    user_resources = resources_with_view_permission.filter(created_by=user)
    if 'filter' in request.GET:
        f = request.GET['filter']
        user_resources = user_resources.filter(url__url_type__url_type__icontains=f).distinct()

    return render_to_response('catalog/results.html', {'results': user_resources, 'created_user': user},
                              context_instance=RequestContext(request))

def category_results(request, category_id):
    category = Category.objects.get(pk=category_id)
    anonymous_user = get_user_model().objects.get(username='AnonymousUser')
    resources_with_view_permission = get_objects_for_user(request.user, 'catalog.view_resource')\
                                     | get_objects_for_user(anonymous_user, 'catalog.view_resource')

    category_resources = resources_with_view_permission.filter(categories=category)
    if 'filter' in request.GET:
        f = request.GET['filter']
        category_resources = category_resources.filter(url__url_type__url_type__icontains=f).distinct()

    return render_to_response('catalog/results.html', {'results': category_resources, 'tag': category},
                              context_instance=RequestContext(request))


def search_results(request):
    anonymous_user = get_user_model().objects.get(username='AnonymousUser')
    resources_with_view_permission = get_objects_for_user(request.user, 'catalog.view_resource')\
                                     | get_objects_for_user(anonymous_user, 'catalog.view_resource')

    search_resources = resources_with_view_permission.order_by("-is_featured", "-created").filter(Q(app__is_suspended=False) | Q(app=None))
    app = None
    app_name = None
    template = 'catalog/results.html'
    if 'qs' in request.GET:
        qs = request.GET['qs'].replace("+", " ")
        search_resources = Resource.search(qs, search_resources).distinct()
    if 'filter' in request.GET:
        f = request.GET['filter']
        search_resources = search_resources.filter(url__url_type__url_type__iexact=f).distinct()
    if 'app' in request.GET:
        template = 'catalog/app_results.html'
        f = request.GET['app']
        app = f
        app_name = core_models.App.objects.get(name=f).title
        search_resources = search_resources.filter(app__name=f).distinct().order_by("-is_featured", "-created")
    return render_to_response(template, {'results': search_resources, 'app': app, 'app_name': app_name},
                              context_instance=RequestContext(request))

@permission_required_or_403('catalog.view_resource', (Resource, 'id', 'resource_id'))
def resource_details(request, resource_id, slug=""):
    resource = get_object_or_404(Resource, pk=resource_id)
    return render_to_response('catalog/details.html', {'resource': resource}, context_instance=RequestContext(request))


"""def idea_results(request, idea_id=None, slug=""):
    if idea_id:
        idea = Idea.objects.get(pk=idea_id)
        return render_to_response('idea_details.html', {'idea': idea}, context_instance=RequestContext(request)) 
    
    ideas = Idea.objects.order_by("-created_by_date")
    return render_to_response('catalog/ideas.html', {'ideas': ideas}, context_instance=RequestContext(request))"""


def feed_list(request):
    tags = Tag.objects.all()
    return render_to_response('catalog/feeds/list.html', {'tags': tags}, context_instance=RequestContext(request))


@superuser_required()
def Save_settings(request, settings_form, permissions_form):
    if settings_form.is_valid() and permissions_form.is_valid():
        for form in permissions_form.forms:
            form.save()
        settings = settings_form.save(commit=False)
        settings.site = Site.objects.get_current()
        settings.save()

        return HttpResponseRedirect(reverse(home))
    else:

        context = {'settings_form': settings_form,
                   'permissions_form': permissions_form}
        return render(request, 'catalog/settings.html', context)


@superuser_required()
def settings(request):
    if (len(Settings.objects.all()) > 0):
        settings_obj = Site.objects.get_current().catalog_settings
    else:
        settings_obj = None
    service_content_type = ContentType.objects.get(app_label="catalog", model="resource")
    perm = Permission.objects.filter(Q(content_type = service_content_type)).filter(Q(codename__contains='add') | Q(codename__contains='delete'))

    if request.method == 'POST':
        settings_form = SettingsForm(request.POST, prefix='settings_form', instance=settings_obj)

        permissions_form = permissions_formset(request.POST, initial=perm)
        return Save_settings(request, settings_form, permissions_form)
    else:
        settings_form = SettingsForm(prefix='settings_form', instance=settings_obj)
        context = {'settings_form': settings_form,
                   'permissions_form': permissions_formset(initial=perm)

        }
        return render(request, 'catalog/settings.html', context)


'''@login_required
def suggest_content(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            #do something
            
            coords, types, formats, updates ="", "", "", ""
            for c in request.POST.getlist("coord_system"):
                coords = coords + " EPSG:" + CoordSystem.objects.get(pk=c).EPSG_code.__str__()
            for t in request.POST.getlist("types"):
                types = types + " " + UrlType.objects.get(pk=t).url_type
            for f in request.POST.getlist("formats"):
                formats = formats + " " + DataType.objects.get(pk=f).data_type
            for u in request.POST.getlist("update_frequency"):
                if u:
                    updates = updates + " " + UpdateFrequency.objects.get(pk=u).update_frequency
                
            data = {
                "submitter": request.user.username,
                "submit_date": datetime.now(),
                "dataset_name": request.POST.get("dataset_name"),
                "organization": request.POST.get("organization"),
                "copyright_holder": request.POST.get("copyright_holder"),
                "contact_email": request.POST.get("contact_email"),
                "contact_phone": request.POST.get("contact_phone"),
                "url": request.POST.get("url"),
                "time_period": request.POST.get("time_period"),
                "release_date": request.POST.get("release_date"),
                "area_of_interest": request.POST.get("area_of_interest"),
                "update_frequency": updates,
                "coord_system": coords,
                "wkt_geometry": request.POST.get("wkt_geometry"),
                "types": types,
                "formats": formats,
                "usage_limitations": request.POST.get("usage_limitations"),
                "collection_process": request.POST.get("collection_process"),
                "data_purpose": request.POST.get("data_purpose"),
                "intended_audience": request.POST.get("intended_audience"),
                "why": request.POST.get("why"),
            }
            
            
            #send_email(request.user, data)
            return render_to_response('catalog/thanks.html', context_instance=RequestContext(request))
    else: 
        form = SubmissionForm()
        
    return render_to_response('catalog/submit.html', {'form': form}, context_instance=RequestContext(request))'''

"""def send_email(user, data):
    subject, user_email = 'OpenDataPhilly - Data Submission', (user.first_name + " " + user.last_name, user.email)
    text_content = render_to_string('submit_email.txt', data)
    text_content_copy = render_to_string('submit_email_copy.txt', data)

    mail_managers(subject, text_content)
    
    msg = EmailMessage(subject, text_content_copy, to=user_email)
    msg.send()
    
    sug_object = Submission()
    sug_object.user = user
    sug_object.email_text = text_content
    
    sug_object.save()

    return sug_object"""



## views called by js ajax for object lists
def get_tag_list(request):
    tags = Tag.objects.all()
    return HttpResponse(serializers.serialize("json", tags))


def get_app_list(request):
    apps = core_models.App.objects.filter(is_suspended=False)
    return HttpResponse(serializers.serialize("json", apps))

##############################################################################################################33
def create_new(request):
    context = {}
    apps = core_models.App.objects.filter(in_menu=True).order_by('order')
    context['apps'] = apps
    return render(request, 'catalog/new_app.html', context)


@csrf_exempt
def validate_url(request):
    exists = False
    if request.method == 'POST':
        resource_url = request.POST.get('url', None)
        if resource_url:
            if Url.objects.filter(url=resource_url).exists():
                exists = True
            else:
                exists = False


    ajax_vars = {'success': True, 'exists': exists}
    return HttpResponse(json.dumps(ajax_vars), mimetype='application/javascript')