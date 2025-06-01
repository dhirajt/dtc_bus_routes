# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from datetime import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0014_auto_20161126_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 2, 15, 42, 53, 417354, tzinfo=timezone.utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='route',
            name='route_type',
            field=models.IntegerField(default=1, choices=[(1, b'DTC'), (2, b'Delhi Transit')]),
        ),
    ]
