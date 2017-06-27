# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

# Create your models here.
class Datalogger(models.Model):
    dat_id=models.AutoField("Id",primary_key=True)
    dat_codigo=models.CharField("Código",max_length=10)
    dat_nombre=models.CharField("Nombre",max_length=25)
    dat_marca=models.CharField("Marca",max_length=25,null=True)
    dat_modelo=models.CharField("Modelo",max_length=25,null=True)
    dat_serial=models.CharField("Serial",max_length=25,null=True)
    dat_estado=models.BooleanField("Estado",default=True)
    def __str__(self):
        return self.dat_nombre
    def get_absolute_url(self):
        return reverse('datalogger:datalogger_detail', kwargs={'pk': self.pk})

class Sensor(models.Model):
    sen_id=models.AutoField("Id",primary_key=True)
    dat_id=models.ForeignKey(
        Datalogger,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Datalogger"
    )
    sen_codigo=models.CharField("Código",max_length=10)
    sen_nombre=models.CharField("Nombre",max_length=20)
    sen_marca=models.CharField("Marca",max_length=20,null=True)
    sen_modelo=models.CharField("Modelo",max_length=20,null=True)
    sen_serial=models.CharField("Serial",max_length=20,null=True)
    sen_estado=models.BooleanField("Estado",default=True)
    def __str__(self):
        return self.sen_nombre
    def get_absolute_url(self):
        return reverse('datalogger:sensor_detail', kwargs={'pk': self.pk})
