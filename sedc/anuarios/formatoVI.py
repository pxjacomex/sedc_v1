# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import RadiacionSolar
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)
from datetime import datetime

class Radiacion(object):
    #matriz multidimensionall de 17 columnas por 12 filas
    maximo=[[0 for x in range(17)] for y in range(12)]
    minimo=[[0 for x in range(17)] for y in range(12)]

def matrizVI(estacion,variable,periodo):
    datos=[]
    obj_estacion=Estacion.objects.get(est_id=estacion)
    obj_rad=Radiacion()
    obj_rad.maximo=rad_max(estacion,variable,periodo)
    obj_rad.minimo=rad_min(estacion,variable,periodo)
    datos=obj_rad
    return datos
def rad_max(estacion,variable,periodo):
    #consulta de maximos, agrupados por hora y por mes
    consulta=(Medicion.objects.filter(est_id=estacion)
        .filter(var_id=variable).filter(med_fecha__year=periodo)
        .filter(med_hora__range=(
            datetime.strptime('05:00:00', '%H:%M:%S').time(),
            datetime.strptime('18:00:00', '%H:%M:%S').time())
        )
        .filter(med_valor__lt=1401)
        .annotate(month=ExtractMonth('med_fecha'),
            hour=ExtractHour('med_hora')
        )
        .values('month','hour')
        .annotate(valor=Max('med_valor'))
        .values('valor','month','hour')
        .order_by('month','hour')
    )
    radiacion=[[0] for i in range(12)]
    for fila in consulta:
        mes=int(fila.get('month'))-1
        radiacion[mes][0]=mes+1
        radiacion[mes].append(round(fila.get('valor'),2))
    for item in range(12):
        radiacion[item].append(max(radiacion[item]))
        radiacion[item].append(radiacion[item].index(max(radiacion[item]))+4)
    #radiacion[1].append(max(radiacion[1]))
    return radiacion
def rad_min(estacion,variable,periodo):
    consulta=(Medicion.objects.filter(est_id=estacion)
        .filter(var_id=variable).filter(med_fecha__year=periodo)
        .filter(med_hora__range=(
            datetime.strptime('05:00:00', '%H:%M:%S').time(),
            datetime.strptime('18:00:00', '%H:%M:%S').time())
        )
        .annotate(month=ExtractMonth('med_fecha'),
            hour=ExtractHour('med_hora')
        )
        .values('month','hour')
        .annotate(valor=Min('med_valor'))
        .values('valor','month','hour')
        .order_by('month','hour')
    )
    radiacion=[[0] for i in range(12)]
    for fila in consulta:
        mes=int(fila.get('month'))-1
        radiacion[mes][0]=mes+1
        radiacion[mes].append(round(fila.get('valor'),2))

    for item in range(12):
        radiacion[item].append(min(radiacion[item]))
        radiacion[item].append(radiacion[item].index(min(radiacion[item]))+4)
    return radiacion

def datos_guardar(estacion,variable,periodo):
    datos=[]
    obj_estacion=Estacion.objects.get(est_id=estacion)
    consulta=(Medicion.objects.filter(est_id=estacion)
        .filter(var_id=variable).filter(med_fecha__year=periodo)
        .filter(med_hora__range=(
            datetime.strptime('05:00:00', '%H:%M:%S').time(),
            datetime.strptime('18:00:00', '%H:%M:%S').time())
        )
        .filter(med_valor__lt=1401)
        .annotate(month=ExtractMonth('med_fecha'),
            hour=ExtractHour('med_hora')
        )
        .values('month','hour')
        .annotate(maximo=Max('med_valor'),minimo=Min('med_valor'))
        .values('maximo','minimo','month','hour')
        .order_by('month','hour')
    )
    for fila in consulta:
        obj_rad=RadiacionSolar()
        obj_rad.est_id=obj_estacion
        obj_rad.rad_periodo=periodo
        obj_rad.rad_mes=fila.get('month')
        obj_rad.rad_hora=fila.get('hour')
        obj_rad.rad_maximo=round(fila.get('maximo'),2)
        obj_rad.rad_minimo=round(fila.get('minimo'),2)
        datos.append(obj_rad)
        print fila.get('maximo')
    return datos
