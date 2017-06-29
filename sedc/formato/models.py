# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from datalogger.models import Datalogger
from variable.models import Variable
from estacion.models import Estacion

# Create your models here.
class Extension(models.Model):
    ext_id=models.AutoField("Id",primary_key=True)
    ext_valor=models.CharField("Valor",max_length=5)
    def __str__(self):
        return self.ext_valor
    def get_absolute_url(self):
        return reverse('formato:extension_detail', kwargs={'pk': self.pk})

class Delimitador(models.Model):
    del_id=models.AutoField("Id",primary_key=True)
    del_valor=models.CharField("Valor",max_length=50)
    del_codigo=models.IntegerField("Código",null=True)
    def __str__(self):
        return self.del_valor
    def get_absolute_url(self):
        return reverse('formato:delimitador_detail', kwargs={'pk': self.pk})

class Formato(models.Model):
    for_id=models.AutoField(primary_key=True)
    ext_id=models.ForeignKey(
        Extension,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Extensión")
    del_id=models.ForeignKey(
        Delimitador,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Delimitador")
    dat_id=models.ForeignKey(
    	Datalogger,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Datalogger")
    for_nombre=models.CharField("Nombre",max_length=50)
    for_descripcion=models.TextField("Descripción",null=True)
    for_ubicacion=models.TextField("Ubicación")
    for_archivo=models.CharField("Archivo",max_length=100,null=True)
    for_num_col=models.IntegerField("Número de columnas")
    for_fil_ini=models.IntegerField("Fila de inicio")
    for_fecha=models.CharField("Formato de fecha",max_length=12)
    for_col_fecha=models.IntegerField("Columna fecha")
    for_hora=models.CharField("Formato de hora",max_length=10)
    for_col_hora=models.IntegerField("Columna de hora")
    for_estado=models.BooleanField("Estado",default=True)
    def __str__(self):
        return self.for_nombre
    def get_absolute_url(self):
        return reverse('formato:formato_detail', kwargs={'pk': self.pk})

class Clasificacion(models.Model):
    cla_id=models.AutoField("Id",primary_key=True)
    for_id=models.ForeignKey(
    	Formato,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Formato")
    var_id=models.ForeignKey(
    	Variable,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Variable")
    cla_valor=models.IntegerField("Valor")
    cla_maximo=models.IntegerField("Máximo valor")
    cla_minimo=models.IntegerField("Mínimo valor")
    def __str__(self):
        return str(self.cla_id)
    def get_absolute_url(self):
        return reverse('formato:clasificacion_detail', kwargs={'pk': self.pk})

class Asociacion(models.Model):
    aso_id=models.AutoField("Id",primary_key=True)
    for_id=models.ForeignKey(
    	Formato,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Formato")
    dat_id=models.ForeignKey(
    	Datalogger,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Datalogger")
    def get_absolute_url(self):
        return reverse('formato:asociacion_detail', kwargs={'pk': self.pk})
