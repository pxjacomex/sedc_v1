# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formato', '0003_auto_20170627_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clasificacion',
            name='cla_maximo',
            field=models.IntegerField(verbose_name='M\xe1ximo valor'),
        ),
        migrations.AlterField(
            model_name='clasificacion',
            name='cla_minimo',
            field=models.IntegerField(verbose_name='M\xednimo valor'),
        ),
        migrations.AlterField(
            model_name='clasificacion',
            name='cla_valor',
            field=models.IntegerField(verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='formato',
            name='for_estado',
            field=models.BooleanField(default=True, verbose_name='Estado'),
        ),
    ]
