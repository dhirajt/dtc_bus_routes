# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field routes on 'Stage'
        db.create_table('rost_stage_routes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stage', models.ForeignKey(orm['rost.stage'], null=False)),
            ('route', models.ForeignKey(orm['rost.route'], null=False))
        ))
        db.create_unique('rost_stage_routes', ['stage_id', 'route_id'])


    def backwards(self, orm):
        # Removing M2M table for field routes on 'Stage'
        db.delete_table('rost_stage_routes')


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
            'latt': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'long': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'routes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rost.Route']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['rost']