# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from datalogger.models import Datalogger
from variable.models import Variable
from estacion.models import Estacion
from marca.models import Marca

# Create your models here.
class Extension(models.Model):
    ext_id=models.AutoField("Id",primary_key=True)
    ext_valor=models.CharField("Valor",max_length=5)
    def __str__(self):
        return self.ext_valor.encode('utf-8')
    def get_absolute_url(self):
        return reverse('formato:extension_detail', kwargs={'pk': self.pk})

class Delimitador(models.Model):
    del_id=models.AutoField("Id",primary_key=True)
    del_nombre=models.CharField("Nombre",max_length=50)
    del_caracter=models.CharField("Caracter",max_length=5)
    def __str__(self):
        return self.del_nombre.encode('utf-8')
    def get_absolute_url(self):
        return reverse('formato:delimitador_detail', kwargs={'pk': self.pk})

class Formato(models.Model):
    TIPO_FECHA=(
    ('%d/%m/%y','DD/MM/YY'),
    ('%m/%d/%y','MM/DD/YY'),
    ('%Y-%m-%d','YYYY-MM-DD'),
    ('"%Y-%m-%d','YYYY-MM-DD'),
    ('%d/%m/%Y','DD/MM/YYYY'),
    ('%m/%d/%Y','MM/DD/YYYY'),
    ('%d-%b-%y','DD-BB-YY'),
    ('%Y-%d-%m','YYYY-DD-MM'),
    ('%d-%m-%Y','DD-MM-YYYY'),
    )
    TIPO_HORA=(
    ('%I:%M:%S %p','HH:MM:SS AM/PM'),
    ('%H:%M:%S','HH:MM:SS 24H'),
    ('%H:%M:%S"','HH:MM:SS 24H'),
    ('%H:%M','HH:MM 24H'),
    )
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
    mar_id=models.ForeignKey(
            Marca,
            models.SET_NULL,
            blank=True,
            null=True,
            verbose_name="Marca Datalogger")
    for_nombre=models.CharField("Nombre",max_length=50)
    for_descripcion=models.TextField("Descripción",null=True)
    for_ubicacion=models.CharField("Ubicación",max_length=300)
    for_archivo=models.CharField("Archivo",max_length=100,blank=True,null=True)
    for_num_col=models.IntegerField("Número de columnas")
    for_fil_ini=models.IntegerField("Fila de inicio")
    for_fecha=models.CharField("Formato de fecha",max_length=12,choices=TIPO_FECHA)
    for_col_fecha=models.IntegerField("Columna fecha")
    for_hora=models.CharField("Formato de hora",max_length=12,choices=TIPO_HORA)
    for_col_hora=models.IntegerField("Columna de hora")
    for_estado=models.BooleanField("Estado",default=True)
    def __str__(self):
        return (self.for_descripcion).encode('utf-8')
    def get_absolute_url(self):
        return reverse('formato:formato_detail', kwargs={'pk': self.pk})
    class Meta:
        ordering=('for_nombre',)

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
    cla_valor=models.IntegerField("Columna valor")
    cla_maximo=models.IntegerField("Columna valor máximo",blank=True,null=True)
    cla_minimo=models.IntegerField("Columna valor mínimo",blank=True,null=True)
    def __str__(self):
        return str(self.cla_id)
    def get_absolute_url(self):
        return reverse('formato:clasificacion_detail', kwargs={'pk': self.pk})
    class Meta:
        ordering=('var_id',)

class Asociacion(models.Model):
    aso_id=models.AutoField("Id",primary_key=True)
    for_id=models.ForeignKey(
    	Formato,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Formato")
    est_id=models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    def get_absolute_url(self):
        return reverse('formato:asociacion_detail', kwargs={'pk': self.pk})
    class Meta:
        ordering=('aso_id',)
