# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ActiveWebPlayer.webplayer'
        db.alter_column(u'webplayer_activewebplayer', 'webplayer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webplayer.WebPlayer'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ActiveWebPlayer.webplayer'
        raise RuntimeError("Cannot reverse this migration. 'ActiveWebPlayer.webplayer' and its values cannot be restored.")

    models = {
        u'webplayer.activewebplayer': {
            'Meta': {'object_name': 'ActiveWebPlayer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'webplayer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webplayer.WebPlayer']", 'null': 'True'})
        },
        u'webplayer.webplayer': {
            'Meta': {'object_name': 'WebPlayer'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['webplayer']