# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 21:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DA', '0007_auto_20170829_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('univers_xuhao', models.IntegerField()),
                ('univers_name', models.CharField(max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DA.City')),
            ],
        ),
    ]
