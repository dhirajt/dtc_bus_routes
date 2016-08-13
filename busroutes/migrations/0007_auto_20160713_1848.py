# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0006_auto_20160713_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='aliases',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name=b'aliases'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='aliases',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name=b'aliases'),
        ),
    ]
