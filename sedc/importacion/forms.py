# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from medicion.models import Medicion
from variable.models import Variable
from datalogger.models import Datalogger
from marca.models import Marca
from datetime import datetime,timedelta
from formato.models import Formato
class UploadFileForm(forms.Form):
    def lista_estaciones():
        lista = ()
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_codigo+str(" ")+item.est_nombre),)
            lista = lista + fila
        return lista
    def lista_formatos():
        lista = ()
        formatos = Formato.objects.all()
        for item in formatos:
            fila = ((str(item.for_id),item.for_descripcion+str(" ")),)
            lista = lista + fila
        return lista
    def lista_datalogger():
        lista = ()
        marcas = Marca.objects.all()
        for item in marcas:
            fila = ((str(item.mar_id),item.mar_nombre),)
            lista = lista + fila
        return lista
    estacion=forms.ChoiceField(choices=lista_estaciones())
    datalogger=forms.ChoiceField(choices=lista_datalogger())
    formato=forms.ChoiceField(choices=lista_formatos())
    sobreescribir=forms.BooleanField(required=False)
    archivo = forms.FileField()
class VaciosForm(forms.Form):
    observacion=forms.CharField(widget=forms.Textarea)
