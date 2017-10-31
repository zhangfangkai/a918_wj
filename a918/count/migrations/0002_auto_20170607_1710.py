# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('count', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jilu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Jilu_shengfen', models.CharField(max_length=200)),
                ('Jilu_daxue', models.CharField(max_length=200)),
                ('Jilu_type', models.CharField(max_length=20)),
                ('Jilu_ml', models.CharField(max_length=200)),
                ('Jilu_xk', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Zyml',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Zyml_name', models.CharField(max_length=200)),
                ('Zyml_bianhao', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Zyxk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Zyxk_name', models.CharField(max_length=200)),
                ('Zyml_id', models.IntegerField()),
                ('Zyxk_bianhao', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='xsml',
            name='Xsml_bianhao',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='xsxk',
            name='Xsxk_bianhao',
            field=models.CharField(max_length=200),
        ),
    ]
