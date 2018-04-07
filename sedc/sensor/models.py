# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from marca.models import Marca

# Create your models here.
class Sensor(models.Model):
    sen_id=models.AutoField("Id",primary_key=True)

    sen_codigo = models.CharField("Código", max_length=10)

    TIPO_NOMBRE=(
        ("Pluviómetro","Pluviómetro"),
        ("Sonda Ultrasónico", "Sonda Ultrasónico" ),
        ("Velocidad del viento", "Velocidad del viento"),
        ("Sonda Piezométrico", "Sonda Piezométrico"),
        ("Humedad y Temperatura", "Humedad y Temperatura"),
        ("Sensor de viento" , "Sensor de viento"),
        ("Sensor de Viento", "Sensor de Viento"),
        ("Pluviómetro", "Pluviómetro"),
        ("Presión Barométrica", "Presión Barométrica"),
        ("Radiación Solar", "Radiación Solar"),
        ("Dirección del viento", "Dirección del viento"),
    )

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
        return self.sen_codigo
    def get_absolute_url(self):
        return reverse('sensor:sensor_detail', kwargs={'pk': self.pk})
    class Meta:
        ordering=('sen_codigo',)