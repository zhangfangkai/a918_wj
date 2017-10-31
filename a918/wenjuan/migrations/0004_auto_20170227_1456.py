# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wenjuan', '0003_auto_20170110_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='wenti',
            name='wenti_xuhao',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='xuanxiang',
            name='xuanxiang_xuhao',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
