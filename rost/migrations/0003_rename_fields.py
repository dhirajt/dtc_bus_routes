# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('rost_stage','latt','lattitude')
	db.rename_column('rost_stage','long','longitude')

    def backwards(self, orm):
        db.rename_column('rost_stage','lattitude','latt')
	db.rename_column('rost_stage','longitude','long')

    models = {
        'rost.route': {
            'Meta': {'object_name': 'Route'},
            'end': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'end'", 'to': "orm['rost.Stage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'stages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rost.Stage']", 'symmetrical': 'False'}),
            'start': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'start'", 'to': "orm['rost.Stage']"})
        },
        'rost.stage': {
            'Meta': {'object_name': 'Stage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lattitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'routes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rost.Route']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['rost']
