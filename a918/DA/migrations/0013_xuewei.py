# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-10 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DA', '0012_ans_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Xuewei',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xuewei_xuhao', models.IntegerField()),
                ('xuewei_name', models.CharField(max_length=100)),
            ],
        ),
    ]