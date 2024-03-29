# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 20:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Delimitador',
            fields=[
                ('del_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('del_valor', models.CharField(max_length=50, verbose_name='Valor')),
            ],
        ),
        migrations.CreateModel(
            name='Extension',
            fields=[
                ('ext_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('ext_valor', models.CharField(max_length=5, verbose_name='Valor')),
            ],
        ),
        migrations.CreateModel(
            name='Formato',
            fields=[
                ('for_id', models.AutoField(primary_key=True, serialize=False)),
                ('for_nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('for_descripcion', models.TextField(null=True, verbose_name='Descripci\xf3n')),
                ('for_ubicacion', models.TextField(verbose_name='Ubicaci\xf3n')),
                ('for_archivo', models.CharField(max_length=100, null=True, verbose_name='Archivo')),
                ('for_num_col', models.IntegerField(verbose_name='Numero de Columnas')),
                ('for_fil_ini', models.IntegerField(verbose_name='Fila de Inicio')),
                ('for_fecha', models.CharField(max_length=12, verbose_name='Formato de Fecha')),
                ('for_col_fecha', models.IntegerField(verbose_name='Columna Fecha')),
                ('for_hora', models.CharField(max_length=10, verbose_name='Formato de Hora')),
                ('for_col_hora', models.IntegerField(verbose_name='Columna de Hora')),
                ('for_estado', models.BooleanField(verbose_name='Estado')),
                ('del_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='formato.Delimitador', verbose_name='Delimitador')),
                ('ext_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='formato.Extension', verbose_name='Extension')),
            ],
        ),
    ]
