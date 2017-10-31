# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('count', '0005_auto_20170608_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='jilu',
            name='Jilu_tp',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
