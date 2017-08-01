# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.utils import timezone
from estacion.models import Estacion
from formato.models import Formato

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
    imp_fecha=models.DateField("Fecha",null=True)
    imp_hora=models.TimeField("Hora",null=True)
    imp_archivo=models.FileField("Archivo",upload_to='archivos/%Y_%m_%d_%H_%M/')
    imp_sobreescribir=models.NullBooleanField("Sobreescribir",default=False)
    def get_absolute_url(self):
        return reverse('importacion:importacion_detail', kwargs={'pk': self.pk})
    ''''def importar(self,id):
        importacion=Importacion.objects.filter(imp_id=self.pk).values('')
        formato=Formato.objects.filter(for_id=importacion.get('for_id_id')).values('')
        estacion=Estacion.objects.filter(est_id=importacion.get('est_id_id')).values('')
        clasificacion=Clasificacion.filter(for_id=formato=)'''
