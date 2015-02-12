# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'catalog_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'catalog', ['Tag'])

        # Adding model 'Category'
        db.create_table(u'catalog_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'catalog', ['Category'])

        # Adding model 'DataType'
        db.create_table(u'catalog_datatype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'catalog', ['DataType'])

        # Adding model 'UrlType'
        db.create_table(u'catalog_urltype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'catalog', ['UrlType'])

        # Adding model 'UpdateFrequency'
        db.create_table(u'catalog_updatefrequency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_frequency', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'catalog', ['UpdateFrequency'])

        # Adding model 'CoordSystem'
        db.create_table(u'catalog_coordsystem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('EPSG_code', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal(u'catalog', ['CoordSystem'])

        # Adding model 'Resource'
        db.create_table(u'catalog_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.App'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('release_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('time_period', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('division', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('usage', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('contact_email', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('contact_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('updates', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.UpdateFrequency'], null=True, blank=True)),
            ('area_of_interest', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('location_extent', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_by', to=orm['auth.User'])),
            ('last_updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updated_by', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('metadata_contact', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('metadata_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('update_frequency', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('data_formats', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('proj_coord_sys', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wkt_geometry', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('csw_typename', self.gf('django.db.models.fields.CharField')(default='csw:Record', max_length=200)),
            ('csw_schema', self.gf('django.db.models.fields.CharField')(default='http://www.opengis.net/cat/csw/2.0.2', max_length=200)),
            ('csw_mdsource', self.gf('django.db.models.fields.CharField')(default='local', max_length=100)),
            ('csw_xml', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('csw_anytext', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['Resource'])

        # Adding M2M table for field tags on 'Resource'
        m2m_table_name = db.shorten_name(u'catalog_resource_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm[u'catalog.resource'], null=False)),
            ('tag', models.ForeignKey(orm[u'catalog.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resource_id', 'tag_id'])

        # Adding M2M table for field data_types on 'Resource'
        m2m_table_name = db.shorten_name(u'catalog_resource_data_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm[u'catalog.resource'], null=False)),
            ('datatype', models.ForeignKey(orm[u'catalog.datatype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resource_id', 'datatype_id'])

        # Adding M2M table for field coord_sys on 'Resource'
        m2m_table_name = db.shorten_name(u'catalog_resource_coord_sys')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm[u'catalog.resource'], null=False)),
            ('coordsystem', models.ForeignKey(orm[u'catalog.coordsystem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resource_id', 'coordsystem_id'])

        # Adding model 'Provider'
        db.create_table(u'catalog_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'catalog', ['Provider'])

        # Adding model 'ServiceType'
        db.create_table(u'catalog_servicetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Provider'], null=True, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['ServiceType'])

        # Adding model 'Url'
        db.create_table(u'catalog_url', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url_label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.UrlType'], null=True, blank=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Resource'], null=True, blank=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Provider'], null=True, blank=True)),
            ('service_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.ServiceType'], null=True, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['Url'])

        # Adding model 'UrlImage'
        db.create_table(u'catalog_urlimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Url'], null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('source_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['UrlImage'])

        # Adding model 'TwitterCache'
        db.create_table(u'catalog_twittercache', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'catalog', ['TwitterCache'])

        # Adding model 'Settings'
        db.create_table(u'catalog_settings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(related_name='catalog_settings', unique=True, to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('enable_rating', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('resources_per_page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=10)),
        ))
        db.send_create_signal(u'catalog', ['Settings'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'catalog_tag')

        # Deleting model 'Category'
        db.delete_table(u'catalog_category')

        # Deleting model 'DataType'
        db.delete_table(u'catalog_datatype')

        # Deleting model 'UrlType'
        db.delete_table(u'catalog_urltype')

        # Deleting model 'UpdateFrequency'
        db.delete_table(u'catalog_updatefrequency')

        # Deleting model 'CoordSystem'
        db.delete_table(u'catalog_coordsystem')

        # Deleting model 'Resource'
        db.delete_table(u'catalog_resource')

        # Removing M2M table for field tags on 'Resource'
        db.delete_table(db.shorten_name(u'catalog_resource_tags'))

        # Removing M2M table for field data_types on 'Resource'
        db.delete_table(db.shorten_name(u'catalog_resource_data_types'))

        # Removing M2M table for field coord_sys on 'Resource'
        db.delete_table(db.shorten_name(u'catalog_resource_coord_sys'))

        # Deleting model 'Provider'
        db.delete_table(u'catalog_provider')

        # Deleting model 'ServiceType'
        db.delete_table(u'catalog_servicetype')

        # Deleting model 'Url'
        db.delete_table(u'catalog_url')

        # Deleting model 'UrlImage'
        db.delete_table(u'catalog_urlimage')

        # Deleting model 'TwitterCache'
        db.delete_table(u'catalog_twittercache')

        # Deleting model 'Settings'
        db.delete_table(u'catalog_settings')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'catalog.category': {
            'Meta': {'ordering': "['category_name']", 'object_name': 'Category'},
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'catalog.coordsystem': {
            'EPSG_code': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'Meta': {'ordering': "['EPSG_code']", 'object_name': 'CoordSystem'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalog.datatype': {
            'Meta': {'ordering': "['data_type']", 'object_name': 'DataType'},
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'catalog.provider': {
            'Meta': {'object_name': 'Provider'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'catalog.resource': {
            'Meta': {'object_name': 'Resource'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.App']", 'null': 'True', 'blank': 'True'}),
            'area_of_interest': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'contact_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'coord_sys': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['catalog.CoordSystem']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_by'", 'to': u"orm['auth.User']"}),
            'csw_anytext': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'csw_mdsource': ('django.db.models.fields.CharField', [], {'default': "'local'", 'max_length': '100'}),
            'csw_schema': ('django.db.models.fields.CharField', [], {'default': "'http://www.opengis.net/cat/csw/2.0.2'", 'max_length': '200'}),
            'csw_typename': ('django.db.models.fields.CharField', [], {'default': "'csw:Record'", 'max_length': '200'}),
            'csw_xml': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'data_formats': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'data_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['catalog.DataType']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'division': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'last_updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'updated_by'", 'to': u"orm['auth.User']"}),
            'location_extent': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'metadata_contact': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'metadata_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'proj_coord_sys': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['catalog.Tag']", 'null': 'True', 'blank': 'True'}),
            'time_period': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'update_frequency': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updates': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.UpdateFrequency']", 'null': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.TextField', [], {}),
            'wkt_geometry': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'catalog.servicetype': {
            'Meta': {'object_name': 'ServiceType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Provider']", 'null': 'True', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'catalog.settings': {
            'Meta': {'object_name': 'Settings'},
            'enable_rating': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resources_per_page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'catalog_settings'", 'unique': 'True', 'to': u"orm['sites.Site']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'catalog.tag': {
            'Meta': {'ordering': "['tag_name']", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'catalog.twittercache': {
            'Meta': {'object_name': 'TwitterCache'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'catalog.updatefrequency': {
            'Meta': {'ordering': "['update_frequency']", 'object_name': 'UpdateFrequency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update_frequency': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'catalog.url': {
            'Meta': {'object_name': 'Url'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Provider']", 'null': 'True', 'blank': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Resource']", 'null': 'True', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.ServiceType']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.UrlType']", 'null': 'True', 'blank': 'True'})
        },
        u'catalog.urlimage': {
            'Meta': {'object_name': 'UrlImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Url']", 'null': 'True', 'blank': 'True'})
        },
        u'catalog.urltype': {
            'Meta': {'ordering': "['url_type']", 'object_name': 'UrlType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.app': {
            'Meta': {'object_name': 'App'},
            'app_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'author_website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_installed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'licence': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.AppTag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'core.apptag': {
            'Meta': {'object_name': 'AppTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['catalog']