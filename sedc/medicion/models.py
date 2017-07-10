# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from variable.models import Variable
from estacion.models import Estacion
from django.urls import reverse


# Create your models here.
class Medicion(models.Model):
    med_id=models.AutoField("Id",primary_key=True)
    var_id=models.ForeignKey(
    	Variable,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Variable")
    est_id=models.ForeignKey(
    	Estacion,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Estación")
    med_fecha=models.DateField("Fecha")
    med_hora=models.TimeField("Hora")
    med_valor=models.DecimalField("Valor",max_digits=14,decimal_places=6,blank=True,null=True)
    med_maximo=models.DecimalField("Máximo",max_digits=14,decimal_places=6,blank=True,null=True)
    med_minimo=models.DecimalField("Mínimo",max_digits=14,decimal_places=6,blank=True,null=True)
    med_validado=models.DecimalField("Validado",max_digits=14,decimal_places=6,blank=True,null=True)
    med_estado=models.NullBooleanField("Estado",default=True)
    def __str__(self):
        return str(self.med_valor)
    def get_absolute_url(self):
        return reverse('medicion:medicion_detail', kwargs={'pk': self.pk})

class Validacion(models.Model):
    val_id=models.AutoField("Id",primary_key=True)
    med_id=models.ForeignKey(
    	Medicion,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Medición")
    val_fecha=models.DateField("Fecha")
    val_hora=models.TimeField("Hora")
    val_valor=models.DecimalField("Valor",max_digits=14,decimal_places=6)
    val_maximo=models.DecimalField("Máximo",max_digits=14,decimal_places=6)
    val_minimo=models.DecimalField("Mínimo",max_digits=14,decimal_places=6)
    val_mensaje=models.CharField("Mensaje",max_length=100)
    def get_absolute_url(self):
        return reverse('medicion:validacion_detail', kwargs={'pk': self.pk})
