# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0002_auto_20150711_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='name_slug',
            field=models.SlugField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
