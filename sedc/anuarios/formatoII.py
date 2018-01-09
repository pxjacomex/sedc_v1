# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import Precipitacion
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)

def matrizII(estacion,variable,periodo):
    datos=[]
    obj_estacion=Estacion.objects.get(est_id=estacion)
    consulta=(Medicion.objects.filter(est_id=estacion)
        .filter(var_id=variable).filter(med_fecha__year=periodo)
        .annotate(month=TruncMonth('med_fecha')).values('month'))
    med_mensual=list(consulta.annotate(c=Sum('med_valor')).
        values('c').order_by('month'))
    datos_diarios=list(Medicion.objects
        .filter(est_id=estacion)
        .filter(var_id=variable)
        .filter(med_fecha__year=periodo)
        .annotate(month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha'))
        .values('month','day')
        .annotate(valor=Sum('med_valor'))
        .values('valor','month','day').order_by('month','day'))
    mensual_simple = [d.get('c') for d in med_mensual]
    max24H,maxdia,totdias = maximospre(datos_diarios)
    for i in range(12):
        obj_precipitacion=Precipitacion()
        obj_precipitacion.est_id=obj_estacion
        obj_precipitacion.pre_periodo=periodo
        obj_precipitacion.pre_mes=i+1
        obj_precipitacion.pre_suma=mensual_simple[i]
        obj_precipitacion.pre_maximo=max24H[i]
        obj_precipitacion.pre_maximo_dia=maxdia[i]
        obj_precipitacion.pre_dias=totdias[i]
        datos.append(obj_precipitacion)
    return datos
def maximospre(datos_diarios):
    # retorna maxima precipitacion mensual y en que dia sucedio y cuantos dias hubo precipitacion
    max24H = []
    maxdia = []
    totdias= []
    for i in range(1,13):
        val_max24h=[]
        val_maxdia = []
        val_totdias= []
        for fila in datos_diarios:
            if fila.get('month') == i:
                val_max24h.append(fila.get('valor'))
                val_maxdia.append(fila.get('day'))
        count = 0
        for j in val_max24h:
            if(j>0):
                count+=1
        max24H.append(max(val_max24h))
        maxdia.append(val_maxdia[val_max24h.index(max(val_max24h))])
        totdias.append(count)
    return max24H,maxdia,totdias
def verificarII(estacion,periodo):
    return Precipitacion.objects.filter(est_id=estacion)\
        .filter(pre_periodo=periodo).exists()
