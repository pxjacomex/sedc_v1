# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from medicion.models import Medicion
#from variable.models import Variable
from datalogger.models import Datalogger
from validacion.models import Validacion
from datetime import datetime,timedelta
from formato.models import Formato,Asociacion
from importacion.functions import construir_matriz
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
        formatos = Datalogger.objects.all().distinct('dat_marca')
        for item in formatos:
            fila = ((str(item.dat_id),item.dat_marca),)
            lista = lista + fila
        return lista
    estacion=forms.ChoiceField(choices=lista_estaciones())
    datalogger=forms.ChoiceField(choices=lista_datalogger())
    formato=forms.ChoiceField(choices=lista_formatos())
    sobreescribir=forms.BooleanField(required=False)
    archivo = forms.FileField()
def procesar_archivo(archivo,form):

    try:
        formato=Formato.objects.get(for_id=form.cleaned_data['formato'])
        estacion=Estacion.objects.get(est_id=form.cleaned_data['estacion'])
        sobreescribir=form.cleaned_data['sobreescribir']
        datos=construir_matriz(archivo,formato,estacion)
        valid=validar_fechas(datos)
        message=str("")
        if not valid:
            message="Datos existentes, por favor seleccione la opcion sobreescribir"
    except ValueError:
        valid=False
        messagge="El formato del datalogger no coincide con el archivo"
    return valid,message



#verificar los datos del archivo
def validar_fechas(datos):
    fecha_ini=datos[0].val_fecha
    hora_ini=datos[0].val_hora
    fecha_fin=datos[-1].val_fecha
    hora_fin=datos[-1].val_hora
    consulta=(Medicion.objects
    .filter(est_id=datos[0].est_id_id)
    .filter(var_id=datos[0].var_id_id)
    .filter(med_fecha__range=[fecha_ini,fecha_fin])
    .filter(med_hora__range=[hora_ini,hora_fin]))
    if consulta:
        return False
    return True
