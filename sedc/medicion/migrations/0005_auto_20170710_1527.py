# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicion', '0004_auto_20170710_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicion',
            name='med_estado',
            field=models.NullBooleanField(default=True, verbose_name='Estado'),
        ),
    ]
