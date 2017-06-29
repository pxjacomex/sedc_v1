# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datalogger.models import Sensor
from estacion.models import Estacion
from django.urls import reverse


# Create your models here.
class Unidad(models.Model):
    uni_id=models.AutoField("Id",primary_key=True)
    uni_nombre=models.CharField("Nombre",max_length=50)
    uni_sigla=models.CharField("Sigla",max_length=10)
    def __str__(self):
        return self.uni_nombre.encode('utf-8')
    def get_absolute_url(self):
        return reverse('variable:unidad_detail', kwargs={'pk': self.pk})

class Variable(models.Model):
    var_id=models.AutoField("Id",primary_key=True)
    uni_id=models.ForeignKey(
    	Unidad,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Unidad")
    var_codigo=models.CharField("Código",max_length=6)
    var_nombre=models.CharField("Nombre",max_length=50)
    var_maximo=models.DecimalField("Máximo",max_digits=7,decimal_places=2)
    var_minimo=models.DecimalField("Mínimo",max_digits=7,decimal_places=2)
    var_sos=models.DecimalField("Sos",max_digits=7,decimal_places=2,null=True,blank=True)
    var_err=models.DecimalField("Error",max_digits=7,decimal_places=2,null=True,blank=True)
    var_min=models.DecimalField("Error mínimo",max_digits=7,decimal_places=2,null=True,blank=True)
    var_estado=models.BooleanField("Estado",default=True)
    def __str__(self):
        return self.var_nombre.encode('utf-8')
    def get_absolute_url(self):
        return reverse('variable:variable_detail', kwargs={'pk': self.pk})


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
    	verbose_name="Estación")
    con_fecha_ini=models.DateField("Fecha inicio")
    con_fecha_fin=models.DateField("Fecha fin")
    def get_absolute_url(self):
        return reverse('variable:control_detail', kwargs={'pk': self.pk})
