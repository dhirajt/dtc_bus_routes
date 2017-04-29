# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0013_auto_20161119_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='uid',
            field=models.CharField(default=b'', max_length=50, blank=True),
        ),
    ]
