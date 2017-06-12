# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datalogger.models import Sensor 
from estacion.models import Estacion

# Create your models here.
class Unidad(models.Model):
    uni_id=models.AutoField("Id",primary_key=True)
    uni_nombre=models.CharField("Nombre",max_length=50)
    uni_sigla=models.CharField("Sigla",max_length=10)
class Variable(models.Model):
    var_id=models.AutoField("Id",primary_key=True)
    uni_id=models.ForeignKey(
	Unidad,
	models.SET_NULL,
	blank=True, 
	null=True, 
	verbose_name="Unidad")
    var_codigo=models.CharField("Codigo",max_length=6)
    var_nombre=models.CharField("Nombre",max_length=50)
    var_maximo=models.DecimalField("Maximo",max_digits=18,decimal_places=8)
    var_minimo=models.DecimalField("Minimo",max_digits=18,decimal_places=8)
    var_sos=models.DecimalField("Sos",max_digits=18,decimal_places=8)
    var_err=models.DecimalField("Error",max_digits=18,decimal_places=8)
    var_min=models.DecimalField("Error Minimo",max_digits=18,decimal_places=8)
    var_estado=models.BooleanField("Estado",default=True)
class Control(models.Model):
    con_id=models.AutoField("Id",primary_key=True)
    var_id=models.ForeignKey(
	Variable, 
	models.SET_NULL, 
	blank=True, 
	null=True, 
	verbose_name="Variable")
    sen_id=models.ForeignKey(
	Sensor,
	blank=True, 
	null=True, 
	verbose_name="Sensor")
    est_id=models.ForeignKey(
	Estacion, 
	models.SET_NULL, 
	blank=True, 
	null=True, 
	verbose_name="Estacion")
    con_fecha_ini=models.DateField()
    con_fecha_fin=models.DateField()
