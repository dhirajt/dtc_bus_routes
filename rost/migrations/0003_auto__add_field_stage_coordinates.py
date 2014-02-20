# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Stage.coordinates'
        db.add_column('rost_stage', 'coordinates',
                      self.gf('geoposition.fields.GeopositionField')(default='0,0', max_length=42),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Stage.coordinates'
        db.delete_column('rost_stage', 'coordinates')


    models = {
        'rost.route': {
            'Meta': {'object_name': 'Route'},
            'end': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'end'", 'to': "orm['rost.Stage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'stages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rost.Stage']", 'through': "orm['rost.StageSeq']", 'symmetrical': 'False'}),
            'start': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'start'", 'to': "orm['rost.Stage']"})
        },
        'rost.stage': {
            'Meta': {'object_name': 'Stage'},
            'coordinates': ('geoposition.fields.GeopositionField', [], {'default': "'0,0'", 'max_length': '42'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'routes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rost.Route']", 'symmetrical': 'False'})
        },
        'rost.stageseq': {
            'Meta': {'object_name': 'StageSeq'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rost.Route']"}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rost.Stage']"})
        }
    }

    complete_apps = ['rost']