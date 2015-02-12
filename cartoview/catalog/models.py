import os
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from lxml import etree
from shapely.wkt import loads

from operator import attrgetter
from django.db import models
from django.db.models import Q
from django.conf import settings
from csw_catalog import settings as csw_settings
from django.contrib.auth.models import User, Permission
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from cartoview2.core import models as core_models
from sorl.thumbnail.fields import ImageField
from djangoratings.fields import RatingField
from django.contrib.gis.db import models
from django.contrib.sites.models import Site
from security.models import *
from django.db.models import signals
class Tag(models.Model):
    tag_name = models.CharField(max_length=150)

    def __unicode__(self):
        return '%s' % self.tag_name

    class Meta:
        ordering = ['tag_name']


class Category(models.Model):
    category_name = models.CharField(max_length=150)

    def __unicode__(self):
        return '%s' % self.category_name

    class Meta:
        ordering = ['category_name']

class DataType(models.Model):
    data_type = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.data_type

    class Meta:
        ordering = ['data_type']


class UrlType(models.Model):
    url_type = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.url_type

    class Meta:
        ordering = ['url_type']


class UpdateFrequency(models.Model):
    update_frequency = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.update_frequency

    class Meta:
        ordering = ['update_frequency']


class CoordSystem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    EPSG_code = models.IntegerField(blank=True, help_text="Official EPSG code, numbers only")

    def __unicode__(self):
        return '%s, %s' % (self.EPSG_code, self.name)

    class Meta:
        ordering = ['EPSG_code']
        verbose_name = 'Coordinate system'


class Resource(models.Model,PermissionLevelMixin):
    @classmethod
    def search(cls, qs = None, objs = None):
        if objs == None:
            objs = cls.objects.filter(is_published = True)

        if qs:
            objs = objs.filter(Q(name__icontains=qs) | Q(description__icontains=qs) | Q(organization__icontains=qs) | Q(division__icontains=qs) |
                               Q(tags__in=Tag.objects.filter(tag_name__icontains=qs))|Q(categories__in=Category.objects.filter(category_name__icontains=qs)))

        return objs

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Resource, self).save(*args, **kwargs)

        self.csw_xml = self.gen_csw_xml()
        self.csw_anytext = self.gen_csw_anytext()
        super(Resource, self).save(*args, **kwargs)

    # Basic Info
    class Meta:
        permissions = (
            ("view_resource", "Can view resource"),
            )
    app = models.ForeignKey(core_models.App ,null=True,blank=True)
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255,blank=True)
    release_date = models.DateField(blank=True, null=True)
    time_period = models.CharField(max_length=50, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    division = models.CharField(max_length=255, blank=True)
    usage = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, null=True)
    data_types = models.ManyToManyField(DataType, blank=True, null=True)

    # More Info
    description = models.TextField()
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_email = models.CharField(max_length=255, blank=True)
    contact_url = models.CharField(max_length=255, blank=True)

    updates = models.ForeignKey(UpdateFrequency, null=True, blank=True)
    area_of_interest = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=True, verbose_name="Public")
    location_extent = models.PolygonField('Extent', srid = 4326, null = True, blank = True)
    created_by = models.ForeignKey(User, related_name='created_by')
    last_updated_by = models.ForeignKey(User, related_name='updated_by')
    created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True)
    metadata_contact = models.CharField(max_length=255, blank=True)
    metadata_notes = models.TextField(blank=True)
    coord_sys = models.ManyToManyField(CoordSystem, blank=True, null=True,  verbose_name="Coordinate system")

    rating = RatingField(range=5, can_change_vote=True)

    update_frequency = models.CharField(max_length=255, blank=True)
    data_formats = models.CharField(max_length=255, blank=True)
    proj_coord_sys = models.CharField(max_length=255, blank=True, verbose_name="Coordinate system")

    is_featured = models.BooleanField(default=False,null=False,blank=False)
    # CSW specific properties
    wkt_geometry = models.TextField(blank=True)
    csw_typename = models.CharField(max_length=200,default="csw:Record")
    csw_schema = models.CharField(max_length=200,default="http://www.opengis.net/cat/csw/2.0.2")
    csw_mdsource = models.CharField(max_length=100,default="local")
    csw_xml = models.TextField(blank=True)
    csw_anytext = models.TextField(blank=True)
    objects = models.GeoManager()

    def get_distinct_url_types(self):
        types = []
        for url in self.url_set.all():
            if url.url_type not in types:
                types.append(url.url_type)
        return sorted(types, key=attrgetter('url_type'))

    def get_grouped_urls(self):
        urls = {}
        for utype in UrlType.objects.all():
            urls[utype.url_type] = self.url_set.filter(url_type=utype)
        return urls

    def get_first_image(self):
        images = UrlImage.objects.filter(url__resource=self)
        if images.count() == 0:
            return None
        return images[0]
    def get_last_image(self):
        images = UrlImage.objects.filter(url__resource=self)
        if images.count() == 0:
            return None
        return images.reverse()[0]

    def get_images(self):
        images = UrlImage.objects.filter(url__resource=self)
        if images.count() == 0:
            return None
        return images

    def get_absolute_url(self):
        slug = slugify(self.name)
        return "/resource/%i/%s" % (self.id, slug)

    def __unicode__(self):
        return '%s' % self.name

    # CSW specific properties
    @property
    def csw_identifier(self):
        if not csw_settings.SITEHOST:
            raise RuntimeError('csw_settings.SITEHOST is not set')
        fqrhn = '.'.join((reversed(csw_settings.SITEHOST.split('.'))))
        return 'urn:x-odc:resource:%s::%d' % (fqrhn, self.id)

    @property
    def csw_type(self):
        data_types = self.data_types.values()
        if len(data_types) > 0:
            return data_types[0]['data_type']
        return None

    @property
    def csw_crs(self):
        crs = self.coord_sys.values()
        if len(crs) > 0:
            return crs[0]['name']
        return None

    @property
    def csw_links(self):
        links = []
        for url in self.url_set.all():
            tmp = '%s,%s,%s,%s' % (url.url_label, url.url_type.url_type, 'WWW:DOWNLOAD-1.0-http--download', url.url)
            links.append(tmp)
        abs_url = '%s%s' % (gen_website_url(), self.get_absolute_url())
        link = '%s,%s,%s,%s' % (self.name, self.name, 'WWW:LINK-1.0-http--link', abs_url)
        links.append(link)
        return '^'.join(links)

    @property
    def csw_keywords(self):
        keywords = []
        for keyword in self.tags.values():
            keywords.append(keyword['tag_name'])
        return ','.join(keywords)

    @property
    def csw_creator(self):
        creator = User.objects.filter(username=self.created_by)[0]
        return '%s %s' % (creator.first_name, creator.last_name)

    def gen_csw_xml(self):

        def nspath(ns, element):
            return '{%s}%s' % (ns, element)

        nsmap = {
            'csw': 'http://www.opengis.net/cat/csw/2.0.2',
            'dc' : 'http://purl.org/dc/elements/1.1/',
            'dct': 'http://purl.org/dc/terms/',
            'ows': 'http://www.opengis.net/ows',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        }

        record = etree.Element(nspath(nsmap['csw'], 'Record'), nsmap=nsmap)
        etree.SubElement(record, nspath(nsmap['dc'], 'identifier')).text = self.csw_identifier
        etree.SubElement(record, nspath(nsmap['dc'], 'title')).text = self.name

        if self.csw_type is not None:
            etree.SubElement(record, nspath(nsmap['dc'], 'type')).text = self.csw_type

        for tag in self.tags.all():
            etree.SubElement(record, nspath(nsmap['dc'], 'subject')).text = tag.tag_name

        etree.SubElement(record, nspath(nsmap['dc'], 'format')).text = str(self.data_formats)

        abs_url = '%s%s' % (gen_website_url(), self.get_absolute_url())
        etree.SubElement(record, nspath(nsmap['dct'], 'references'), scheme='WWW:LINK-1.0-http--link').text = abs_url

        for link in self.url_set.all():
            etree.SubElement(record, nspath(nsmap['dct'], 'references'),
                             scheme='WWW:DOWNLOAD-1.0-http--download').text = link.url

        etree.SubElement(record, nspath(nsmap['dct'], 'modified')).text = str(self.last_updated)
        etree.SubElement(record, nspath(nsmap['dct'], 'abstract')).text = self.description

        etree.SubElement(record, nspath(nsmap['dc'], 'date')).text = str(self.created)
        etree.SubElement(record, nspath(nsmap['dc'], 'creator')).text = str(self.csw_creator)

        etree.SubElement(record, nspath(nsmap['dc'], 'coverage')).text = self.area_of_interest

        try:
            # geom = loads(self.wkt_geometry)
            # bounds = geom.envelope.bounds
            # dimensions = str(geom.envelope._ndim)
            bounds = self.location_extent.extent
            dimensions = str(self.location_extent.dims)
            bbox = etree.SubElement(record, nspath(nsmap['ows'], 'BoundingBox'), dimensions=dimensions)

            if self.csw_crs is not None:
                bbox.attrib['crs'] = self.csw_crs

            etree.SubElement(bbox, nspath(nsmap['ows'], 'LowerCorner')).text = '%s %s' % (bounds[1], bounds[0])
            etree.SubElement(bbox, nspath(nsmap['ows'], 'UpperCorner')).text = '%s %s' % (bounds[3], bounds[2])
        except Exception:
            # We can safely ignore geom issues
            pass

        return etree.tostring(record)

    def gen_csw_anytext(self):
        xml = etree.fromstring(self.csw_xml)
        return ' '.join([value.strip() for value in xml.xpath('//text()')])

    def set_tags(self, tags):
        tags=filter(None, tags)
        for tag in self.tags.all():
            if tag.tag_name not in tags:
                self.tags.remove(tag)
                if (len(tag.resource_set.all())==0):
                    tag.delete()
        if (len(tags)==0):
            pass
        else:
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(tag_name=tag_name)
                self.tags.add(tag)
                del tag , created
    def get_tags (self):
        tags_list = self.tags.all()
        all_tags = []
        if len(tags_list)> 0:
            for tag in tags_list:
                all_tags.append(tag.tag_name)

            return  ",".join(all_tags)
        else:
            return None
        
    def set_categories(self, categories):
        categories=filter(None, categories)
        for category in self.categories.all():
            if category.category_name not in categories:
                self.categories.remove(category)
                if (len(category.resource_set.all())==0):
                    category.delete()
        if (len(categories)==0):
            pass
        else:
            for category_name in categories:
                category, created = category.objects.get_or_create(category_name=category_name)
                self.categorys.add(category)
                del category , created
    def get_categories (self):
        categories_list = self.categories.all()
        all_categories = []
        if len(categories_list)> 0:
            for category in categories_list:
                all_categories.append(category.category_name)

            return  ",".join(all_categories)
        else:
            return None

    def add_urls(self,urls):
        """
        urls is list of dicts , each dict represent url :

        [ {'url': , 'label': , 'url_type': , 'thumbnail_name': , 'thumbnail_img': },
        {'url': , 'label': , 'url_type': , 'thumbnail_name': , 'thumbnail_img': },
        {'url': , 'label': , 'url_type': , 'thumbnail_name': , 'thumbnail_img': } ]

        """
        for url in urls:
            url_type, created = UrlType.objects.get_or_create(url_type=url['url_type'])
            url_obj = Url(url = url['url'] , url_type = url_type ,url_label = url['label'],resource=self )
            if (('service_type' in url)):
                if (('provider' in url)):
                    provider = Provider.objects.get(provider=url['provider'])
                    url_obj.provider = provider
                    service_type = ServiceType.objects.get(service_type= url['service_type'],provider = provider)
                else:
                     service_type, created = ServiceType.objects.get_or_create(service_type= url['service_type'])
                url_obj.service_type = service_type
            url_obj.save()
            if ( ('thumbnail_name' in url) and ('thumbnail_img' in url) ):
                url_thumbnail = UrlImage(url=url_obj)
                url_thumbnail.image = url['thumbnail_img']
                url_thumbnail.title = url['thumbnail_name']
                url_thumbnail.save()

    def set_missing_info(self):
        """Set default permissions and point of contacts.

           It is mandatory to call it from descendant classes
           but hard to enforce technically via signals or save overriding.
        """
        from guardian.models import UserObjectPermission
        #  True if every key in the get_all_level_info dict is empty.
        no_custom_permissions = UserObjectPermission.objects.filter(
            content_type=ContentType.objects.get_for_model(self.get_self_resource()),
            object_pk=str(self.pk)
            ).count()

        if no_custom_permissions == 0:
            self.set_default_permissions()

class Provider (models.Model):
    provider = models.CharField(max_length=50)
    def __unicode__(self):
        return '%s' %(self.provider)
class ServiceType (models.Model):
    def only_filename(instance, filename):
        return filename

    image = ImageField(upload_to=only_filename, help_text="The site will resize this master image as necessary for page display", blank=True, null = True)

    service_type = models.CharField(max_length=50)
    provider = models.ForeignKey(Provider,null=True,blank=True)

    def __unicode__(self):
        return '%s'%(self.service_type)
class Url(models.Model):
    url = models.CharField(max_length=255)
    url_label = models.CharField(max_length=255)
    url_type = models.ForeignKey(UrlType,null=False,blank=False)
    resource = models.ForeignKey(Resource,null=True,blank=True)
    provider = models.ForeignKey(Provider,null=True,blank=True)
    service_type = models.ForeignKey(ServiceType,null=True,blank=True)
    def __unicode__(self):
        return '%s - %s - %s' % (self.url_label, self.url_type, self.url)


class UrlImage(models.Model):
    def only_filename(instance, filename):
        return filename

    url = models.ForeignKey(Url,null=True,blank=True)
    image = ImageField(upload_to=only_filename, help_text="The site will resize this master image as necessary for page display", blank=True)
    title = models.CharField(max_length=255, help_text="For image alt tags", blank=True)
    source = models.CharField(max_length=255, help_text="Source location or person who created the image", blank=True)
    source_url = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return '%s' % (self.image)


def gen_website_url():
    return csw_settings.SITE_URL

class TwitterCache(models.Model):
    text = models.TextField()


TYPES_CHOICES = (
        ("all", ("All resources")),
        ("featured", ("Featured resources")))
class Settings(models.Model):
    site = models.OneToOneField(Site , related_name='catalog_settings')
    title = models.CharField(max_length=255, blank=True)
    enable_rating = models.BooleanField(default=True)
    show_tags_panel = models.BooleanField(default=True)
    show_categories_panel = models.BooleanField(default=True)
    resources_per_page = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    default_view = models.CharField(max_length=255, blank=True ,choices=TYPES_CHOICES)
def resourcebase_post_save(instance, *args, **kwargs):
    """
    Used to fill any additional fields after the save.
    Has to be called by the children
    """
    instance.set_missing_info()
def get_permitted (permission):
    try:
        group = Group.objects.get( permissions=permission)
        permitted_group = group
    except:
        permitted_group = None
    try :
        users = User.objects.filter( Q(user_permissions=permission) ).distinct()
        permitted_users = users
    except:
        permitted_users = None

    return permitted_users , permitted_group
def set_default_perms(**kwargs):
    service_content_type = ContentType.objects.get(app_label="catalog", model="resource")
    perms = Permission.objects.filter(Q(content_type = service_content_type)).filter(Q(codename__contains='add') | Q(codename__contains='delete'))
    registered_group = Group.objects.get(name='registered')
    for perm in perms :
        users , groups = get_permitted(perm)
        if (not (groups or  users)):
            registered_group.permissions.add(perm)

signals.post_save.connect(resourcebase_post_save, sender=Resource)
#signals.post_syncdb.connect(set_default_perms)