# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0007_auto_20160713_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='route_type',
            field=models.IntegerField(default=1, choices=[(1, b'DTC'), (2, b'Cluster')]),
        ),
    ]
