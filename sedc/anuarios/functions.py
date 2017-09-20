# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import TemperaturaAire
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)

from anuarios.formatoI import matrizI
from anuarios.formatoII import matrizII
from anuarios.formatoIII import matrizIII
from anuarios.formatoIV import matrizIV
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
    return datos
def guardar_variable(datos):
    for obj_variable in datos:
        obj_variable.save()

def template(variable):
    template='anuarios/tai.html'
    if variable=="1":
        template='anuarios/pre.html'
    elif variable=="2":
        template='anuarios/tai.html'
    elif variable=="3":
        template='anuarios/hai.html'
    elif variable=="6":
        template='anuarios/hsu.html'
    elif variable=="8":
        template='anuarios/pat.html'
    elif variable=="9":
        template='anuarios/tag.html'
    elif variable=="10":
        template='anuarios/cau.html'
    elif variable=="11":
        template='anuarios/nag.html'
    return template
