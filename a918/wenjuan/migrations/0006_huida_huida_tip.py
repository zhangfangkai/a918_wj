# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wenjuan', '0005_huida'),
    ]

    operations = [
        migrations.AddField(
            model_name='huida',
            name='huida_tip',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]
