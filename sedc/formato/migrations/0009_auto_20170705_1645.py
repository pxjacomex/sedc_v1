# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formato', '0008_auto_20170630_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formato',
            name='for_ubicacion',
            field=models.CharField(max_length=300, verbose_name='Ubicaci\xf3n'),
        ),
    ]
