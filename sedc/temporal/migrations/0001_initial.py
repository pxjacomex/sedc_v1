# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-30 12:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datos',
            fields=[
                ('med_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('var_id', models.IntegerField(verbose_name='Variable')),
                ('est_id', models.IntegerField(verbose_name='Estaci\xf3n')),
                ('med_fecha', models.DateField(verbose_name='Fecha')),
                ('med_hora', models.TimeField(verbose_name='Hora')),
                ('med_valor', models.DecimalField(blank=True, decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('med_maximo', models.DecimalField(blank=True, decimal_places=6, max_digits=14, null=True, verbose_name='M\xe1ximo')),
                ('med_minimo', models.DecimalField(blank=True, decimal_places=6, max_digits=14, null=True, verbose_name='M\xednimo')),
                ('med_validado', models.DecimalField(blank=True, decimal_places=6, max_digits=14, null=True, verbose_name='Validado')),
                ('med_estado', models.NullBooleanField(default=True, verbose_name='Estado')),
            ],
        ),
    ]
