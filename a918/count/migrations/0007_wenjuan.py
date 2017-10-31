# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('count', '0006_jilu_jilu_tp'),
    ]

    operations = [
        migrations.CreateModel(
            name='wenjuan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wenjuan_name', models.CharField(max_length=200)),
                ('wenjuan_url', models.CharField(max_length=200)),
            ],
        ),
    ]
