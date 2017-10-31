# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('count', '0008_wenjuan_wenjuan_tuijian'),
    ]

    operations = [
        migrations.AddField(
            model_name='wenjuan',
            name='wenjuan_status',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
