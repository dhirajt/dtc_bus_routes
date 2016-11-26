# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0010_route_uid'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='route',
            unique_together=set([('name', 'direction', 'start_stage', 'end_stage', 'route_type'), ('name', 'direction', 'route_type')]),
        ),
    ]
