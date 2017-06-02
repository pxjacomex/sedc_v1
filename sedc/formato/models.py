# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Extension(models.Model):
    ext_id=models.AutoField("Id",primary_key=True)
    ext_valor=models.CharField("Valor",max_length=5)

class Delimitador(models.Model):
    del_id=models.AutoField("Id",primary_key=True)
    del_valor=models.CharField("Valor",max_length=50)
class Formato(models.Model):
    for_id=models.AutoField(primary_key=True)
    ext_id=models.ForeignKey(
        Extension,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Extension")
    del_id=models.ForeignKey(
        Delimitador,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Delimitador"
    )
    for_nombre=models.CharField("Nombre",max_length=50)
    for_descripcion=models.TextField("Descripción",null=True)
    for_ubicacion=models.TextField("Ubicación")
    for_archivo=models.CharField("Archivo",max_length=100,null=True)
    for_num_col=models.IntegerField("Numero de Columnas")
    for_fil_ini=models.IntegerField("Fila de Inicio")
    for_fecha=models.CharField("Formato de Fecha",max_length=12)
    for_col_fecha=models.IntegerField("Columna Fecha")
    for_hora=models.CharField("Formato de Hora",max_length=10)
    for_col_hora=models.IntegerField("Columna de Hora")
    for_estado=models.BooleanField("Estado")
