# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0009_auto_20160717_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='uid',
            field=models.CharField(default=b'', max_length=10, blank=True),
        ),
    ]
