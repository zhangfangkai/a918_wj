# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wenjuan', '0002_wenti_xuanxiang'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wenjuan',
            old_name='user_name',
            new_name='user_id',
        ),
    ]
