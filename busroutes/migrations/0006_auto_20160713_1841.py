# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('busroutes', '0005_route_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stagesequence',
            options={'ordering': ['sequence'], 'verbose_name': 'Stage Sequence', 'verbose_name_plural': 'Stage Sequences'},
        ),
        migrations.AddField(
            model_name='route',
            name='aliases',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='stage',
            name='aliases',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='stage',
            name='uid',
            field=models.CharField(default=b'', max_length=10),
        ),
        migrations.AlterField(
            model_name='route',
            name='direction',
            field=models.CharField(default=b'U', max_length=1, choices=[(b'U', b'Up'), (b'D', b'Down')]),
        ),
    ]
