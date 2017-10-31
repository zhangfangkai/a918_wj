# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Daxue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('daxue_name', models.CharField(max_length=200)),
                ('shengfen_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Shengfen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shengfen_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Xsml',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Xsml_name', models.CharField(max_length=200)),
                ('Xsml_bianhao', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Xsxk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Xsxk_name', models.CharField(max_length=200)),
                ('Xsml_id', models.IntegerField()),
                ('Xsxk_bianhao', models.IntegerField()),
            ],
        ),
    ]
