# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from estacion.models import Estacion

class Precipitacion(models.Model):
    pre_id=models.AutoField(primary_key=True)
    est_id=models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    pre_periodo=models.IntegerField("Año")
    pre_mes=models.IntegerField("Mes")
    pre_suma=models.DecimalField("Precipitación",max_digits=7,decimal_places=2)
    pre_maximo=models.DecimalField("Máximo en 24H",max_digits=7,decimal_places=2)
    pre_maximo_dia=models.IntegerField("Día")
    pre_dias=models.IntegerField("Total de días con precipitacion")

class TemperaturaAire(models.Model):
    tai_id=models.AutoField(primary_key=True)
    est_id=models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    tai_periodo=models.IntegerField("Año",default=2000)
    tai_mes=models.IntegerField("Mes")
    tai_maximo_abs=models.DecimalField("Máximo Absoluto",max_digits=7,decimal_places=2)
    tai_maximo_dia=models.IntegerField("Día")
    tai_minimo_abs=models.DecimalField("Mínimo Absoluto",max_digits=7,decimal_places=2)
    tai_minimo_dia=models.IntegerField("Día")
    tai_maximo=models.DecimalField("Máximo",max_digits=7,decimal_places=2)
    tai_minimo=models.DecimalField("Mínimo",max_digits=7,decimal_places=2)
    tai_promedio=models.DecimalField("Promedio",max_digits=7,decimal_places=2)
    class Meta:
        ordering=('tai_mes',)
