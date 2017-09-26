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
from anuarios.formatoVI import matrizVI,datos_guardar
from anuarios.formatoV import matrizV
def calcular(form):
    datos=[]
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
        datos=matrizV(estacion,variable,periodo)
    elif int(variable) in typeVI:
        datos=matrizVI(estacion,variable,periodo)
    return datos
def guardar_variable(datos,form):
    estacion=form.cleaned_data['estacion']
    variable=form.cleaned_data['variable']
    periodo=form.cleaned_data['periodo']
    if verficar_anuario(estacion,variable,periodo):
        if variable=="7":
            radiacion=datos_guardar(estacion,variable,periodo)
            for rad in radiacion:
                rad.save()
        else:
            for obj_variable in datos:
                obj_variable.save()
def verficar_anuario(estacion,variable,periodo):
    result=True
    if variable=="1":
        consulta=models.Precipitacion.objects.filter(est_id=estacion)\
        .filter(per_periodo=periodo)
    elif variable=="2":
        consulta=models.TemperaturaAire.objects.filter(est_id=estacion)\
        .filter(tai_periodo=periodo)
    elif variable=="3":
        consulta=models.HumedadAire.objects.filter(est_id=estacion)\
        .filter(hai_periodo=periodo)
    elif variable=="6":
        consulta=models.HumedadSuelo.objects.filter(est_id=estacion)\
        .filter(hai_periodo=periodo)
    elif variable=="7":
        consulta=models.RadiacionSolar.objects.filter(est_id=estacion)\
        .filter(rad_periodo=periodo)
    elif variable=="8":
        consulta=models.PresionAtmosferica.objects.filter(est_id=estacion)\
        .filter(pat_periodo=periodo)
    elif variable=="9":
        consulta=models.TemperaturaAgua.objects.filter(est_id=estacion)\
        .filter(tag_periodo=periodo)
    elif variable=="10":
        consulta=models.Caudal.objects.filter(est_id=estacion)\
        .filter(cau_periodo=periodo)
    elif variable=="11":
        consulta=models.NivelAgua.objects.filter(est_id=estacion)\
        .filter(nag_periodo=periodo)
    if consulta.count()>0:
        result=False
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
