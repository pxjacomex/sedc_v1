# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios import models
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)

from anuarios.formatoI import matrizI
from anuarios.formatoII import matrizII
from anuarios.formatoIII import matrizIII
from anuarios.formatoIV import matrizIV
from anuarios.formatoV import datos_viento,matrizV_mensual
from anuarios.formatoVI import matrizVI,datos_guardar, datos_radiacion_maxima,datos_radiacion_minimo
def calcular(form):
    datos=[]
    valid=False
    typeI = [6,8,9,10,11]
    typeII = [1]
    typeIII = [2]
    typeIV = [3]
    typeV = [4,5]
    typeVI = [7]
    estacion=form.cleaned_data['estacion']
    variable=form.cleaned_data['variable']
    periodo=form.cleaned_data['periodo']
    if int(variable) in typeI:
        datos=matrizI(estacion,variable,periodo)
    elif int(variable) in typeII:
        datos=matrizII(estacion,variable,periodo)
    elif int(variable) in typeIII:
        datos=matrizIII(estacion,variable,periodo)
    elif int(variable) in typeIV:
        datos=matrizIV(estacion,variable,periodo)
    elif int(variable) in typeV:
        datos=matrizV_mensual(estacion,variable,periodo)
    elif int(variable) in typeVI:
        datos=matrizVI(estacion,variable,periodo)
    return datos
def guardar_variable(datos,form):
    estacion=form.cleaned_data['estacion']
    variable=form.cleaned_data['variable']
    periodo=form.cleaned_data['periodo']
    if verficar_anuario(estacion,variable,periodo):
        borrar_datos(estacion,variable,periodo)
    if variable=="7":
        datos_radiacion_maxima(datos,estacion,periodo)
        datos_radiacion_minimo(datos,estacion,periodo)
    elif variable=="4" or variable=="5":
        viento=datos_viento(datos,estacion,periodo)
        for obj_viento in viento:
            obj_viento.save()
    else:
        for obj_variable in datos:
            obj_variable.save()
def borrar_datos(estacion,variable,periodo):
    if variable=="1":
        result=models.Precipitacion.objects.filter(est_id=estacion)\
        .filter(pre_periodo=periodo).delete()
    elif variable=="2":
        result=models.TemperaturaAire.objects.filter(est_id=estacion)\
        .filter(tai_periodo=periodo).delete()
    elif variable=="3":
        result=models.HumedadAire.objects.filter(est_id=estacion)\
        .filter(hai_periodo=periodo).delete()
    elif variable=="4" or variable=="5":
        result=models.Viento.objects.filter(est_id=estacion)\
        .filter(vie_periodo=periodo).delete()
    elif variable=="6":
        result=models.HumedadSuelo.objects.filter(est_id=estacion)\
        .filter(hsu_periodo=periodo).delete()
    elif variable=="7":
        result=models.RadiacionMaxima.objects.filter(est_id=estacion)\
        .filter(rad_periodo=periodo).delete()
        result=models.RadiacionMinima.objects.filter(est_id=estacion)\
        .filter(rad_periodo=periodo).delete()
    elif variable=="8":
        result=models.PresionAtmosferica.objects.filter(est_id=estacion)\
        .filter(pat_periodo=periodo).delete()
    elif variable=="9":
        result=models.TemperaturaAgua.objects.filter(est_id=estacion)\
        .filter(tag_periodo=periodo).delete()
    elif variable=="10":
        result=models.Caudal.objects.filter(est_id=estacion)\
        .filter(cau_periodo=periodo).delete()
    elif variable=="11":
        result=models.NivelAgua.objects.filter(est_id=estacion)\
        .filter(nag_periodo=periodo).delete()
def verficar_anuario(estacion,variable,periodo):
    result=False
    if variable=="1":
        result=models.Precipitacion.objects.filter(est_id=estacion)\
        .filter(pre_periodo=periodo).exists()
    elif variable=="2":
        result=models.TemperaturaAire.objects.filter(est_id=estacion)\
        .filter(tai_periodo=periodo).exists()
    elif variable=="3":
        result=models.HumedadAire.objects.filter(est_id=estacion)\
        .filter(hai_periodo=periodo).exists()
    elif variable=="4":
        result=models.Viento.objects.filter(est_id=estacion)\
        .filter(vie_periodo=periodo).exists()
    elif variable=="5":
        result=models.Viento.objects.filter(est_id=estacion)\
        .filter(vie_periodo=periodo).exists()
    elif variable=="6":
        result=models.HumedadSuelo.objects.filter(est_id=estacion)\
        .filter(hsu_periodo=periodo)
    elif variable=="7":
        result=models.RadiacionMaxima.objects.filter(est_id=estacion)\
        .filter(rad_periodo=periodo).exists()
        result=models.RadiacionMinima.objects.filter(est_id=estacion)\
        .filter(rad_periodo=periodo).exists()
    elif variable=="8":
        result=models.PresionAtmosferica.objects.filter(est_id=estacion)\
        .filter(pat_periodo=periodo).exists()
    elif variable=="9":
        result=models.TemperaturaAgua.objects.filter(est_id=estacion)\
        .filter(tag_periodo=periodo).exists()
    elif variable=="10":
        result=models.Caudal.objects.filter(est_id=estacion)\
        .filter(cau_periodo=periodo).exists()
    elif variable=="11":
        result=models.NivelAgua.objects.filter(est_id=estacion)\
        .filter(nag_periodo=periodo).exists()
    return result
def template(variable):
    template='anuarios/tai.html'
    if variable=="1":
        template='anuarios/pre.html'
    elif variable=="2":
        template='anuarios/tai.html'
    elif variable=="3":
        template='anuarios/hai.html'
    elif variable=="4":
        template='anuarios/vvi.html'
    elif variable=="5":
        template='anuarios/dvi.html'
    elif variable=="6":
        template='anuarios/hsu.html'
    elif variable=="7":
        template='anuarios/rad.html'
    elif variable=="8":
        template='anuarios/pat.html'
    elif variable=="9":
        template='anuarios/tag.html'
    elif variable=="10":
        template='anuarios/cau.html'
    elif variable=="11":
        template='anuarios/nag.html'
    return template
