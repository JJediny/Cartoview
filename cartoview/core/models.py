import os

from django.contrib.gis.db import models
from django.contrib.auth.models import User , Group
from allauth.account.signals import user_signed_up
from django.contrib.sites.models import Site
from django.db.models.signals import post_save ,m2m_changed
from django.dispatch import receiver
from sorl.thumbnail.fields import ImageField
from cartoview2.core.apps_helper import delete_installed_app
from djangoratings.fields import RatingField

current_folder, filename = os.path.split(os.path.abspath(__file__))
temp_dir = os.path.join(current_folder,'temp')
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class HomePage(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.title

@receiver(user_signed_up)
def new_user_signup(sender, **kwargs):
    p = UserProfile(user = kwargs['user'])
    p.save()

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """ This method is executed whenever an user object is saved
    """

    if instance:
        registered_group, reg_created = Group.objects.get_or_create(name='registered')
        instance.groups.add(registered_group)
        if instance.is_staff:
            admin_group, admin_created = Group.objects.get_or_create(name='admin')
            instance.groups.add(admin_group)

class AppTag(models.Model):
    name = models.CharField(max_length=200, unique=True, null=True, blank=True)

    def __unicode__(self):
        return self.name


class App(models.Model):
    def only_filename(instance, filename):
        return filename

    name = models.CharField(max_length=200, unique=True, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    app_url = models.URLField(null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    author_website = models.URLField(null=True, blank=True)
    license = models.CharField(max_length=200, null=True, blank=True)
    tags = models.ManyToManyField(AppTag, null=True, blank=True)
    date_installed = models.DateTimeField('Date Installed', auto_now_add=True)
    installed_by = models.ForeignKey(User, null=True, blank=True)
    single_instance = models.BooleanField(default=False, null=False, blank=False)
    order = models.SmallIntegerField(null=False, blank=False, default=0)
    owner_url = models.URLField(null=True, blank=True)
    help_url = models.URLField(null=True, blank=True)
    app_logo = ImageField(upload_to=only_filename, help_text="The site will resize this master image as necessary for page display", blank=True, null = True)
    is_suspended = models.NullBooleanField(null=True, blank=True , default= False)
    app_img = ImageField(upload_to=only_filename, help_text="The site will resize this master image as necessary for page display", blank=True, null = True)
    in_menu = models.NullBooleanField(null=True, blank=True , default= True)
    rating = RatingField(range=5, can_change_vote=True)
    contact_name = models.CharField(max_length=200, null=True, blank=True)
    contact_email = models.EmailField (null=True, blank=True)

    def delete(self):
        delete_installed_app(self)
        super(type(self), self).delete()


    def __unicode__(self):
        return self.title


def only_filename(instance, filename):
    return filename


class AppInstance(models.Model):
    app = models.ForeignKey(App,null=True,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to=only_filename, null=True,blank=True)
    date_installed = models.DateTimeField("Date Installed",auto_now_add=True)
    owner = models.ForeignKey(User,null=True, blank=True)
    location_extent = models.PolygonField('Extent', srid = 4326, null = True, blank = True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.title


class KeyValueGroup(models.Model):
    name = models.CharField(max_length=200,unique=True)

    def __unicode__(self):
        return self.name

#TODO support data types (string/int/float/bool/etc...)
class KeyValue(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200,null=True)
    group = models.ForeignKey(KeyValueGroup)


    def __unicode__(self):
        name = '%s_%s' % (self.group.name, self.key)
        return name.replace(' ','_').lower()

class Settings(models.Model):
    site = models.OneToOneField(Site , related_name='cartoview_settings')
    show_home_logo = models.BooleanField(default=True)
