# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('count', '0002_auto_20170607_1710'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Zyml',
            new_name='Zylx',
        ),
        migrations.RenameModel(
            old_name='Zyxk',
            new_name='Zyly',
        ),
        migrations.RenameField(
            model_name='zylx',
            old_name='Zyml_bianhao',
            new_name='Zylx_bianhao',
        ),
        migrations.RenameField(
            model_name='zylx',
            old_name='Zyml_name',
            new_name='Zylx_name',
        ),
        migrations.RenameField(
            model_name='zyly',
            old_name='Zyxk_bianhao',
            new_name='Zyly_bianhao',
        ),
        migrations.RenameField(
            model_name='zyly',
            old_name='Zyml_id',
            new_name='Zyly_id',
        ),
        migrations.RenameField(
            model_name='zyly',
            old_name='Zyxk_name',
            new_name='Zyly_name',
        ),
    ]
