# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WebPlayer'
        db.create_table(u'webplayer_webplayer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'webplayer', ['WebPlayer'])

        # Adding model 'ActiveWebPlayer'
        db.create_table(u'webplayer_activewebplayer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('webplayer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webplayer.WebPlayer'])),
        ))
        db.send_create_signal(u'webplayer', ['ActiveWebPlayer'])


    def backwards(self, orm):
        # Deleting model 'WebPlayer'
        db.delete_table(u'webplayer_webplayer')

        # Deleting model 'ActiveWebPlayer'
        db.delete_table(u'webplayer_activewebplayer')


    models = {
        u'webplayer.activewebplayer': {
            'Meta': {'object_name': 'ActiveWebPlayer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'webplayer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webplayer.WebPlayer']"})
        },
        u'webplayer.webplayer': {
            'Meta': {'object_name': 'WebPlayer'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['webplayer']