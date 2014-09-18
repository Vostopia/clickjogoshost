# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'WebPlayer.progressbarframe_image'
        db.alter_column(u'webplayer_webplayer', 'progressbarframe_image', self.gf('apps.s3direct.fields.S3DirectField')())

        # Changing field 'WebPlayer.logo_image'
        db.alter_column(u'webplayer_webplayer', 'logo_image', self.gf('apps.s3direct.fields.S3DirectField')())

        # Changing field 'WebPlayer.file'
        db.alter_column(u'webplayer_webplayer', 'file', self.gf('apps.s3direct.fields.S3DirectField')())

        # Changing field 'WebPlayer.progressbar_image'
        db.alter_column(u'webplayer_webplayer', 'progressbar_image', self.gf('apps.s3direct.fields.S3DirectField')())

    def backwards(self, orm):

        # Changing field 'WebPlayer.progressbarframe_image'
        db.alter_column(u'webplayer_webplayer', 'progressbarframe_image', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'WebPlayer.logo_image'
        db.alter_column(u'webplayer_webplayer', 'logo_image', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'WebPlayer.file'
        db.alter_column(u'webplayer_webplayer', 'file', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'WebPlayer.progressbar_image'
        db.alter_column(u'webplayer_webplayer', 'progressbar_image', self.gf('django.db.models.fields.files.FileField')(max_length=100))

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
            'file': ('apps.s3direct.fields.S3DirectField', [], {}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '575'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_image': ('apps.s3direct.fields.S3DirectField', [], {'blank': 'True'}),
            'progressbar_image': ('apps.s3direct.fields.S3DirectField', [], {'blank': 'True'}),
            'progressbarframe_image': ('apps.s3direct.fields.S3DirectField', [], {'blank': 'True'}),
            'textcolor': ('django.db.models.fields.CharField', [], {'default': "'000000'", 'max_length': '16'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '800'})
        }
    }

    complete_apps = ['webplayer']