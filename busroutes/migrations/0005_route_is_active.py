# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0004_route_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
