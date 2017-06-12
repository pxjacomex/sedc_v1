# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from variable.models import Variable
from estacion.models import Estacion

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
	verbose_name="Estacion")
    med_fecha=models.DateField()
    med_hora=models.TimeField()
    med_valor=models.DecimalField("Valor",max_digits=18,decimal_places=8)
    med_maximo=models.DecimalField("Maximo",max_digits=18,decimal_places=8)
    med_minimo=models.DecimalField("Minimo",max_digits=18,decimal_places=8)
    med_validado=models.DecimalField("Validado",max_digits=18,decimal_places=8)
    med_estado=models.BooleanField("Estado",default=True)
class Validacion(models.Model):
    val_id=models.AutoField("Id",primary_key=True)
    med_id=models.ForeignKey(
	Medicion, 
	models.SET_NULL, 
	blank=True, 
	null=True, 
	verbose_name="Medicion")
    val_fecha=models.DateField()
    val_hora=models.TimeField()
    val_valor=models.DecimalField("Valor",max_digits=18,decimal_places=8)
    val_maximo=models.DecimalField("Maximo",max_digits=18,decimal_places=8)
    val_minimo=models.DecimalField("Minimo",max_digits=18,decimal_places=8)
    val_mensaje=models.CharField("Validado",max_length=100)
