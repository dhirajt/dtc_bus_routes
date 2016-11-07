# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0008_route_route_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='frequency',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='route',
            name='aliases',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name=b'aliases'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='aliases',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name=b'aliases'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='uid',
            field=models.CharField(default=b'', max_length=10, blank=True),
        ),
    ]
