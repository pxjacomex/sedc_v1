# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-27 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importacion', '0003_importacion_mar_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importacion',
            name='imp_archivo',
            field=models.FileField(upload_to='documents/', verbose_name='Archivo'),
        ),
    ]