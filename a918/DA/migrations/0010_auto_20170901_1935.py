# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-01 19:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DA', '0009_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='cho_con',
            new_name='score_con',
        ),
    ]
