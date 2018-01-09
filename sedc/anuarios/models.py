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

class HumedadAire(models.Model):
    hai_id=models.AutoField(primary_key=True)
    est_id=models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    hai_periodo=models.IntegerField("Año",default=2000)
    hai_mes=models.IntegerField("Mes")
    hai_maximo=models.DecimalField("Máximo Absoluto",max_digits=7,decimal_places=2)
    hai_maximo_dia=models.IntegerField("Día")
    hai_minimo=models.DecimalField("Máximo Absoluto",max_digits=7,decimal_places=2)
    hai_minimo_dia=models.IntegerField("Día")
    hai_promedio=models.DecimalField("Máximo Absoluto",max_digits=7,decimal_places=2)
    class Meta:
        ordering=('hai_mes',)
class HumedadSuelo(models.Model):
    hsu_id=models.AutoField(primary_key=True)
    est_id=models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    hsu_periodo=models.IntegerField("Año",default=2000)
    hsu_mes=models.IntegerField("Mes")
    hsu_maximo=models.DecimalField("Máximo",max_digits=7,decimal_places=2)
    hsu_minimo=models.DecimalField("Mínimo",max_digits=7,decimal_places=2)
    hsu_promedio=models.DecimalField("Promedio",max_digits=7,decimal_places=2)
    class Meta:
        ordering=('hsu_mes',)
class RadiacionSolar(models.Model):
    rad_id=models.AutoField(primary_key=True)
    est_id=models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    rad_periodo=models.IntegerField("Año",default=2000)
    rad_mes=models.IntegerField("Mes")
    rad_hora=models.IntegerField("Hora")
    rad_maximo=models.DecimalField("Máximo",max_digits=7,decimal_places=2)
    rad_minimo=models.DecimalField("Mínimo",max_digits=7,decimal_places=2)
class PresionAtmosferica(models.Model):
    pat_id=models.AutoField(primary_key=True)
    est_id=models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    pat_periodo=models.IntegerField("Año",default=2000)
    pat_mes=models.IntegerField("Mes")
    pat_maximo=models.DecimalField("Máximo",max_digits=7,decimal_places=2)
    pat_minimo=models.DecimalField("Mínimo",max_digits=7,decimal_places=2)
    pat_promedio=models.DecimalField("Promedio",max_digits=7,decimal_places=2)
    class Meta:
        ordering=('pat_mes',)
class TemperaturaAgua(models.Model):
    tag_id=models.AutoField(primary_key=True)
    est_id=models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    tag_periodo=models.IntegerField("Año",default=2000)
    tag_mes=models.IntegerField("Mes")
    tag_maximo=models.DecimalField("Máximo",max_digits=7,decimal_places=2)
    tag_minimo=models.DecimalField("Mínimo",max_digits=7,decimal_places=2)
    tag_promedio=models.DecimalField("Promedio",max_digits=7,decimal_places=2)
    class Meta:
        ordering=('tag_mes',)
class Caudal(models.Model):
    cau_id=models.AutoField(primary_key=True)
    est_id=models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    cau_periodo=models.IntegerField("Año",default=2000)
    cau_mes=models.IntegerField("Mes")
    cau_maximo=models.DecimalField("Máximo",max_digits=7,decimal_places=2)
    cau_minimo=models.DecimalField("Mínimo",max_digits=7,decimal_places=2)
    cau_promedio=models.DecimalField("Promedio",max_digits=7,decimal_places=2)
    class Meta:
        ordering=('cau_mes',)
class NivelAgua(models.Model):
    nag_id=models.AutoField(primary_key=True)
    est_id=models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    nag_periodo=models.IntegerField("Año",default=2000)
    nag_mes=models.IntegerField("Mes")
    nag_maximo=models.DecimalField("Máximo",max_digits=7,decimal_places=2)
    nag_minimo=models.DecimalField("Mínimo",max_digits=7,decimal_places=2)
    nag_promedio=models.DecimalField("Promedio",max_digits=7,decimal_places=2)
    class Meta:
        ordering=('nag_mes',)
