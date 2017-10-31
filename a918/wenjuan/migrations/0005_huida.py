# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wenjuan', '0004_auto_20170227_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='Huida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wenjuan_id', models.IntegerField()),
                ('wenti_id', models.IntegerField()),
                ('huida_data', models.CharField(max_length=1000)),
            ],
        ),
    ]
