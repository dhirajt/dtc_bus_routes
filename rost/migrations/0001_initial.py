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
            ('latt', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('long', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('rost', ['Stage'])

        # Adding model 'Route'
        db.create_table('rost_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('start', self.gf('django.db.models.fields.related.ForeignKey')(related_name='start', to=orm['rost.Stage'])),
            ('end', self.gf('django.db.models.fields.related.ForeignKey')(related_name='end', to=orm['rost.Stage'])),
        ))
        db.send_create_signal('rost', ['Route'])

        # Adding M2M table for field stages on 'Route'
        db.create_table('rost_route_stages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('route', models.ForeignKey(orm['rost.route'], null=False)),
            ('stage', models.ForeignKey(orm['rost.stage'], null=False))
        ))
        db.create_unique('rost_route_stages', ['route_id', 'stage_id'])


    def backwards(self, orm):
        # Deleting model 'Stage'
        db.delete_table('rost_stage')

        # Deleting model 'Route'
        db.delete_table('rost_route')

        # Removing M2M table for field stages on 'Route'
        db.delete_table('rost_route_stages')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['rost']