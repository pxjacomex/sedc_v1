# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-09 18:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anuarios', '0008_viento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viento',
            name='vie_direccion',
        ),
        migrations.RemoveField(
            model_name='viento',
            name='vie_porcentaje',
        ),
        migrations.RemoveField(
            model_name='viento',
            name='vie_promedio',
        ),
    ]
