# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-15 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0002_auto_20180315_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logmedicion',
            name='med_fecha',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha'),
        ),
    ]
