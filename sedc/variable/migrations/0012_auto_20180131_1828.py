# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-31 18:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('variable', '0011_auto_20180131_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='sen_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sensor.Sensor', verbose_name='Sensor'),
        ),
    ]
