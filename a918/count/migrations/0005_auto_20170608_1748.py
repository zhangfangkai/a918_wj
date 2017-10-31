# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('count', '0004_auto_20170608_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xsxk',
            name='Xsxk_bianhao',
        ),
        migrations.RemoveField(
            model_name='zyly',
            name='Zyly_bianhao',
        ),
    ]
