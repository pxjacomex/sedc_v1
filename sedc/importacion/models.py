# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.utils import timezone
from estacion.models import Estacion
from formato.models import Formato
from marca.models import Marca
import time

class Importacion(models.Model):
    imp_id=models.AutoField("Id",primary_key=True)
    est_id=models.ForeignKey(
    	Estacion,
    	models.SET_NULL,
    	blank=True,
    	null=True,
    	verbose_name="Estación")
    for_id=models.ForeignKey(
        Formato,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Formato"
    )
    imp_fecha=models.DateTimeField("Fecha",default=time.strftime('%Y-%m-%d %H:%M:%S'))
    imp_fecha_ini=models.DateTimeField("Fecha Inicial",default=time.strftime('%Y-%m-%d %H:%M:%S'))
    imp_fecha_fin=models.DateTimeField("Fecha Final",default=time.strftime('%Y-%m-%d %H:%M:%S'))
    imp_archivo=models.FileField("Archivo",upload_to='archivos/')
    def get_absolute_url(self):
        return reverse('importacion:importacion_detail', kwargs={'pk': self.pk})
