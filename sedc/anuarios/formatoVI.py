# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import RadiacionSolar,RadiacionMaxima, RadiacionMinima
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
    obj_estacion=estacion.est_id.objects.get(est_id=estacion.est_id)
    obj_rad=Radiacion()
    obj_rad.maximo=rad_max(estacion,variable,periodo)
    obj_rad.minimo=rad_min(estacion,variable,periodo)
    datos=obj_rad
    return datos
def rad_max(estacion,variable,periodo):
    #consulta de maximos, agrupados por hora y por mes
    consulta=(Medicion.objects.filter(est_id=estacion.est_id)
        .filter(var_id=variable.var_id).filter(med_fecha__year=periodo)
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
    obj_rad_max=RadiacionMaxima()
    for fila in consulta:
        mes=int(fila.get('month'))-1
        radiacion[mes][0]=mes+1
        radiacion[mes].append(round(fila.get('valor'),2))
    for item in range(12):
        radiacion[item].append(max(radiacion[item]))
        radiacion[item].append(radiacion[item].index(max(radiacion[item]))+4)
    return radiacion
def rad_min(estacion,variable,periodo):
    consulta=(Medicion.objects.filter(est_id=estacion.est_id)
        .filter(var_id=variable.var_id).filter(med_fecha__year=periodo)
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
    obj_estacion=estacion.est_id.objects.get(est_id=estacion.est_id)
    consulta=(Medicion.objects.filter(est_id=estacion.est_id)
        .filter(var_id=variable.var_id).filter(med_fecha__year=periodo)
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
def datos_radiacion_maxima(datos,estacion,periodo):
    lista=[]
    obj_estacion=estacion.est_id.objects.get(est_id=estacion.est_id)
    for fila in datos.maximo:
        obj_rad_max=RadiacionMaxima()
        obj_rad_max.est_id=obj_estacion
        obj_rad_max.rad_periodo=periodo
        obj_rad_max.rad_mes=fila[0]
        obj_rad_max.rad_5=fila[1]
        obj_rad_max.rad_6=fila[2]
        obj_rad_max.rad_7=fila[3]
        obj_rad_max.rad_8=fila[4]
        obj_rad_max.rad_9=fila[5]
        obj_rad_max.rad_10=fila[6]
        obj_rad_max.rad_11=fila[7]
        obj_rad_max.rad_12=fila[8]
        obj_rad_max.rad_13=fila[9]
        obj_rad_max.rad_14=fila[10]
        obj_rad_max.rad_15=fila[11]
        obj_rad_max.rad_16=fila[12]
        obj_rad_max.rad_17=fila[13]
        obj_rad_max.rad_18=fila[14]
        obj_rad_max.rad_max=fila[15]
        obj_rad_max.rad_hora=fila[16]
        obj_rad_max.save()
def datos_radiacion_minimo(datos,estacion,periodo):
    lista=[]
    obj_estacion=estacion.est_id.objects.get(est_id=estacion.est_id)
    for fila in datos.minimo:
        obj_rad_min=RadiacionMinima()
        obj_rad_min.est_id=obj_estacion
        obj_rad_min.rad_periodo=periodo
        obj_rad_min.rad_mes=fila[0]
        obj_rad_min.rad_5=fila[1]
        obj_rad_min.rad_6=fila[2]
        obj_rad_min.rad_7=fila[3]
        obj_rad_min.rad_8=fila[4]
        obj_rad_min.rad_9=fila[5]
        obj_rad_min.rad_10=fila[6]
        obj_rad_min.rad_11=fila[7]
        obj_rad_min.rad_12=fila[8]
        obj_rad_min.rad_13=fila[9]
        obj_rad_min.rad_14=fila[10]
        obj_rad_min.rad_15=fila[11]
        obj_rad_min.rad_16=fila[12]
        obj_rad_min.rad_17=fila[13]
        obj_rad_min.rad_18=fila[14]
        obj_rad_min.rad_max=fila[15]
        obj_rad_min.rad_hora=fila[16]
        obj_rad_min.save()
