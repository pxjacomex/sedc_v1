# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-26 14:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formato', '0019_auto_20180126_1020'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FechaHora',
        ),
        migrations.AlterModelOptions(
            name='formato',
            options={'ordering': ('for_id',)},
        ),
    ]
