# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'core_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['UserProfile'])

        # Adding model 'AppTag'
        db.create_table(u'core_apptag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['AppTag'])

        # Adding model 'App'
        db.create_table(u'core_app', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('app_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('author_website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('licence', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('date_installed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('installed_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['App'])

        # Adding M2M table for field tags on 'App'
        m2m_table_name = db.shorten_name(u'core_app_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('app', models.ForeignKey(orm[u'core.app'], null=False)),
            ('apptag', models.ForeignKey(orm[u'core.apptag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['app_id', 'apptag_id'])

        # Adding model 'AppInstance'
        db.create_table(u'core_appinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.App'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('date_installed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('location_extent', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['AppInstance'])

        # Adding model 'KeyValueGroup'
        db.create_table(u'core_keyvaluegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'core', ['KeyValueGroup'])

        # Adding model 'KeyValue'
        db.create_table(u'core_keyvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.KeyValueGroup'])),
        ))
        db.send_create_signal(u'core', ['KeyValue'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'core_userprofile')

        # Deleting model 'AppTag'
        db.delete_table(u'core_apptag')

        # Deleting model 'App'
        db.delete_table(u'core_app')

        # Removing M2M table for field tags on 'App'
        db.delete_table(db.shorten_name(u'core_app_tags'))

        # Deleting model 'AppInstance'
        db.delete_table(u'core_appinstance')

        # Deleting model 'KeyValueGroup'
        db.delete_table(u'core_keyvaluegroup')

        # Deleting model 'KeyValue'
        db.delete_table(u'core_keyvalue')


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
        u'core.appinstance': {
            'Meta': {'object_name': 'AppInstance'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.App']", 'null': 'True', 'blank': 'True'}),
            'date_installed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_extent': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'core.apptag': {
            'Meta': {'object_name': 'AppTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'core.keyvalue': {
            'Meta': {'object_name': 'KeyValue'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.KeyValueGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'core.keyvaluegroup': {
            'Meta': {'object_name': 'KeyValueGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'core.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['core']