__author__ = 'AmrAbdelaziz'

from django import template
from cartoview2.core.models import App
from django.contrib.auth.models import  User, Permission
from cartoview2.urls import urlpatterns
register = template.Library()

@register.filter('can_edit')
def can_edit(app_name):
    import_string = "from apps."+app_name +".permissions import edit_perm"
    exec import_string
    edit_perm = app_name + '.' + edit_perm()
    return edit_perm

@register.filter('can_add')
def can_add(app_name):
    try:
        import_string = "from apps."+app_name +".permissions import add_perm"
        exec import_string
        add_perm = app_name + '.' +add_perm()
        return add_perm
    except:
        return None

@register.filter
def can_delete(app_name):
    #delete_function =getattr(getattr(getattr(__import__('apps'), app_name) , 'permissions'),'delete_perm')
    import_string = "from apps."+app_name +".permissions import delete_perm"
    exec import_string
    delete_perm = app_name + '.'  + delete_perm()
    return str(delete_perm)

@register.filter
def has_add(username): #check if user has at least one add permission , also return true if an app found to have no permissions
    user = User.objects.get(username = username)
    apps = App.objects.filter(is_suspended = False).filter(in_menu=True)
    has_add_perm = False
    # add_resource_perm = Permission.objects.get(codename='add_resource')
    # if user.has_perm(add_resource_perm):
    #     has_add_perm = True
    #     return has_add_perm
    for app in apps:
        import_string = "from apps."+app.name +".permissions import add_perm"
        try:
            exec import_string
            add_perm = app.name + '.' +add_perm()
            if user.has_perm(add_perm):
                has_add_perm = True
                break
        except:
            has_add_perm = True

    return has_add_perm

@register.filter
def has_no_perms(app_name):
    #delete_function =getattr(getattr(getattr(__import__('apps'), app_name) , 'permissions'),'delete_perm')
    import_string = "from apps."+app_name +".permissions import add_perm"
    try:
        exec import_string
        return False
    except:
        return True


@register.filter
def url_exists(url):
  for e in urlpatterns:
    if e.regex.match(url):
        #or do whatever you want
        return  True        #then exit the procedure.
  return False