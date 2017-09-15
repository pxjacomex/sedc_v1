# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import TemperaturaAire
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)

from anuarios.formatoII import matrizII
from anuarios.formatoIII import matrizIII
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
    if int(variable) in typeII:
        datos=matrizII(estacion,variable,periodo)
    elif int(variable) in typeIII:
        datos=matrizIII(estacion,variable,periodo)
    return datos
def guardar_variable(datos):
    for obj_variable in datos:
        obj_variable.save()

def template(variable):
    typeI = [6,8,9,10,11]
    typeII = [1]
    typeIII = [2]
    typeIV = [3]
    typeV = [4,5]
    typeVI = [7]
    template='anuarios/tai.html'
    if int(variable) in typeII:
        template='anuarios/pre.html'
    if int(variable) in typeIII:
        template='anuarios/tai.html'
    return template
