# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0003_stage_name_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 15, 16, 35, 39, 777710, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
