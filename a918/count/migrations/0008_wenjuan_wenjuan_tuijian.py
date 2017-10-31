# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('count', '0007_wenjuan'),
    ]

    operations = [
        migrations.AddField(
            model_name='wenjuan',
            name='wenjuan_tuijian',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
