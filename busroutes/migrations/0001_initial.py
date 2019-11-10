# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusRouteTiming',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField()),
                ('is_ac', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Bus Route Timing',
                'verbose_name_plural': 'Bus Route Timings',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('direction', models.CharField(max_length=2)),
                ('ac_bus_available', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Route',
                'verbose_name_plural': 'Routes',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('coordinates', geoposition.fields.GeopositionField(max_length=42)),
            ],
            options={
                'verbose_name': 'Stage',
                'verbose_name_plural': 'Stages',
            },
        ),
        migrations.CreateModel(
            name='StageSequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sequence', models.IntegerField()),
                ('route', models.ForeignKey(to='busroutes.Route', on_delete=models.DO_NOTHING)),
                ('stage', models.ForeignKey(to='busroutes.Stage', on_delete=models.DO_NOTHING)),
            ],
            options={
                'verbose_name': 'Stage Sequence',
                'verbose_name_plural': 'Stage Sequences',
            },
        ),
        migrations.AddField(
            model_name='route',
            name='end_stage',
            field=models.ForeignKey(related_name='end_stage', to='busroutes.Stage', on_delete=models.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='route',
            name='stages',
            field=models.ManyToManyField(to='busroutes.Stage', through='busroutes.StageSequence'),
        ),
        migrations.AddField(
            model_name='route',
            name='start_stage',
            field=models.ForeignKey(related_name='start_stage', to='busroutes.Stage', on_delete=models.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='busroutetiming',
            name='route',
            field=models.ForeignKey(to='busroutes.Route', on_delete=models.DO_NOTHING),
        ),
        migrations.AlterUniqueTogether(
            name='stagesequence',
            unique_together=set([('route', 'stage', 'sequence')]),
        ),
        migrations.AlterUniqueTogether(
            name='route',
            unique_together=set([('name', 'start_stage', 'end_stage'), ('name', 'direction')]),
        ),
        migrations.AlterUniqueTogether(
            name='busroutetiming',
            unique_together=set([('route', 'time', 'is_ac')]),
        ),
    ]
