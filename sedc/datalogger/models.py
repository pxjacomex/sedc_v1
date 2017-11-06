# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from estacion.models import Estacion
from marca.models import Marca

# Create your models here.
class Datalogger(models.Model):
    dat_id=models.AutoField("Id",primary_key=True)
    est_id=models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    dat_codigo=models.CharField("Código",max_length=10)
    mar_id=models.ForeignKey(
        Marca,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Marca"
    )
    dat_modelo=models.CharField("Modelo",max_length=25,null=True)
    dat_serial=models.CharField("Serial",max_length=25,null=True)
    dat_estado=models.BooleanField("Estado",default=True)
    def __str__(self):
        return self.dat_codigo
    def get_absolute_url(self):
        return reverse('datalogger:datalogger_detail', kwargs={'pk': self.pk})
    class Meta:
        ordering=('dat_codigo',)

"""class Sensor(models.Model):
    TIPO_NOMBRE=(
        ('Termómetro','Termómetro'),
        ('Higrómetro','Higrómetro'),
        ('Pluviógrafo','Pluviógrafo'),
        ('Veleta','Veleta'),
        ('Anemómetro','Anemómetro'),
        ('Barómetro','Barómetro'),
        ('TDR','TDR'),
        ('Piranómetro','Piranómetro'),
        ('Termómetro de agua','Termómetro de agua'),
        ('Sensor de nivel','Sensor de nivel'),
    )
    sen_id=models.AutoField("Id",primary_key=True)
    sen_nombre=models.CharField("Nombre",max_length=20,choices=TIPO_NOMBRE)
    mar_id=models.ForeignKey(
        Marca,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Marca"
    )
    sen_modelo=models.CharField("Modelo",max_length=20,null=True)
    sen_serial=models.CharField("Serial",max_length=20,null=True)
    sen_estado=models.BooleanField("Estado",default=True)

    def __str__(self):
        return (self.sen_nombre + " " + self.sen_modelo + " " + self.sen_serial).encode('utf-8')
    def get_absolute_url(self):
        return reverse('datalogger:sensor_detail', kwargs={'pk': self.pk})
    class Meta:
        ordering=('sen_nombre','sen_modelo','sen_serial',)"""
