# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Estacion(models.Model):
    TIPO_ESTACION=(
        ('M','Meteorológica'),
        ('P','Pluviométrica'),
        ('H','Hidrológica'),
        )
    est_id=models.AutoField("Id",primary_key=True)
    est_codigo=models.CharField("Código",max_length=10)
    est_nombre=models.CharField("Nombre",max_length=100)
    est_tipo=models.CharField("Tipo",max_length=25,choices=TIPO_ESTACION)
    est_estado=models.BooleanField("Activo",default=True)
    est_provincia=models.CharField("Provincia",max_length=50,null=True)
    est_latitud=models.DecimalField("Latitud",max_digits=10,decimal_places=2,null=True)
    est_longitud=models.DecimalField("Longitud",max_digits=10,decimal_places=2,null=True)
    est_altura=models.IntegerField("Altura",null=True,validators=[MaxValueValidator(6000), MinValueValidator(0)])
    est_ficha=models.FileField("Fichas",upload_to='documents/')
    def __str__(self):
        return self.est_codigo.encode('utf-8')
    def get_absolute_url(self):
        return reverse('estacion:estacion_detail', kwargs={'pk': self.pk})
    class Meta:
        ordering=('est_id',)

'''class Registro(models.Model):
    reg_id=models.AutoField("Id",primary_key=True)
    est_id=models.ForeignKey(
    	Estacion,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Estación")
    reg_fecha=models.DateField("Fecha",null=True)
    reg_archivo=models.CharField("Archivo",max_length=50, null=True)
    reg_ubicacion=models.CharField("Ubicación",max_length=200, null=True)
    def get_absolute_url(self):
        return reverse('estacion:registro_detail', kwargs={'pk': self.pk})'''
