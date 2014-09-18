# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WebPlayer.width'
        db.add_column(u'webplayer_webplayer', 'width',
                      self.gf('django.db.models.fields.IntegerField')(default=800),
                      keep_default=False)

        # Adding field 'WebPlayer.height'
        db.add_column(u'webplayer_webplayer', 'height',
                      self.gf('django.db.models.fields.IntegerField')(default=575),
                      keep_default=False)

        # Adding field 'WebPlayer.backgroundcolor'
        db.add_column(u'webplayer_webplayer', 'backgroundcolor',
                      self.gf('django.db.models.fields.CharField')(default='FFFFFF', max_length=16),
                      keep_default=False)

        # Adding field 'WebPlayer.bordercolor'
        db.add_column(u'webplayer_webplayer', 'bordercolor',
                      self.gf('django.db.models.fields.CharField')(default='FFFFFF', max_length=16),
                      keep_default=False)

        # Adding field 'WebPlayer.textcolor'
        db.add_column(u'webplayer_webplayer', 'textcolor',
                      self.gf('django.db.models.fields.CharField')(default='000000', max_length=16),
                      keep_default=False)

        # Adding field 'WebPlayer.logo_image'
        db.add_column(u'webplayer_webplayer', 'logo_image',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'WebPlayer.progressbar_image'
        db.add_column(u'webplayer_webplayer', 'progressbar_image',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'WebPlayer.progressbarframe_image'
        db.add_column(u'webplayer_webplayer', 'progressbarframe_image',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WebPlayer.width'
        db.delete_column(u'webplayer_webplayer', 'width')

        # Deleting field 'WebPlayer.height'
        db.delete_column(u'webplayer_webplayer', 'height')

        # Deleting field 'WebPlayer.backgroundcolor'
        db.delete_column(u'webplayer_webplayer', 'backgroundcolor')

        # Deleting field 'WebPlayer.bordercolor'
        db.delete_column(u'webplayer_webplayer', 'bordercolor')

        # Deleting field 'WebPlayer.textcolor'
        db.delete_column(u'webplayer_webplayer', 'textcolor')

        # Deleting field 'WebPlayer.logo_image'
        db.delete_column(u'webplayer_webplayer', 'logo_image')

        # Deleting field 'WebPlayer.progressbar_image'
        db.delete_column(u'webplayer_webplayer', 'progressbar_image')

        # Deleting field 'WebPlayer.progressbarframe_image'
        db.delete_column(u'webplayer_webplayer', 'progressbarframe_image')


    models = {
        u'webplayer.activewebplayer': {
            'Meta': {'object_name': 'ActiveWebPlayer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'webplayer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webplayer.WebPlayer']", 'null': 'True'})
        },
        u'webplayer.webplayer': {
            'Meta': {'object_name': 'WebPlayer'},
            'backgroundcolor': ('django.db.models.fields.CharField', [], {'default': "'FFFFFF'", 'max_length': '16'}),
            'bordercolor': ('django.db.models.fields.CharField', [], {'default': "'FFFFFF'", 'max_length': '16'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '575'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'progressbar_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'progressbarframe_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'textcolor': ('django.db.models.fields.CharField', [], {'default': "'000000'", 'max_length': '16'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '800'})
        }
    }

    complete_apps = ['webplayer']