# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wenjuan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wenti',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wenti_name', models.CharField(max_length=200)),
                ('wenjuan_id', models.IntegerField()),
                ('wenti_type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Xuanxiang',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wenti_id', models.IntegerField()),
                ('xuanxiang_name', models.CharField(max_length=200)),
            ],
        ),
    ]
