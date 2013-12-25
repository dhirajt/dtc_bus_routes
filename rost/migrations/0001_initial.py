# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stage'
        db.create_table('rost_stage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('lattitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('rost', ['Stage'])

        # Adding M2M table for field routes on 'Stage'
        db.create_table('rost_stage_routes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stage', models.ForeignKey(orm['rost.stage'], null=False)),
            ('route', models.ForeignKey(orm['rost.route'], null=False))
        ))
        db.create_unique('rost_stage_routes', ['stage_id', 'route_id'])

        # Adding model 'Route'
        db.create_table('rost_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('start', self.gf('django.db.models.fields.related.ForeignKey')(related_name='start', to=orm['rost.Stage'])),
            ('end', self.gf('django.db.models.fields.related.ForeignKey')(related_name='end', to=orm['rost.Stage'])),
        ))
        db.send_create_signal('rost', ['Route'])

        # Adding model 'StageSeq'
        db.create_table('rost_stageseq', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rost.Route'])),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rost.Stage'])),
            ('sequence', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('rost', ['StageSeq'])


    def backwards(self, orm):
        # Deleting model 'Stage'
        db.delete_table('rost_stage')

        # Removing M2M table for field routes on 'Stage'
        db.delete_table('rost_stage_routes')

        # Deleting model 'Route'
        db.delete_table('rost_route')

        # Deleting model 'StageSeq'
        db.delete_table('rost_stageseq')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lattitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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