# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('count', '0003_auto_20170607_1718'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zyly',
            old_name='Zyly_id',
            new_name='Zylx_id',
        ),
    ]
