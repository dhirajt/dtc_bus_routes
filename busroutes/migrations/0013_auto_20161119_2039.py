# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0012_auto_20161119_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='uid',
            field=models.CharField(default=b'', max_length=20, blank=True),
        ),
    ]
