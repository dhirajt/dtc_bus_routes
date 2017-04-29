# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0011_auto_20161119_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
