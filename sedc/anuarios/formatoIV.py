# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import HumedadAire
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)
def matrizIV(estacion,variable,periodo):
    datos=[]
    obj_estacion=Estacion.objects.get(est_id=estacion)
    consulta=Medicion.objects.filter(est_id=estacion)\
    .filter(var_id=variable).filter(med_fecha__year=periodo)\
    .annotate(month=TruncMonth('med_fecha')).values('month')

    datos_diarios_max=list(Medicion.objects
        .filter(est_id=estacion)
        .filter(var_id=variable)
        .filter(med_fecha__year=periodo)
        .exclude(med_valor=0)
        .annotate(month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha'))
        .values('month','day')
        .annotate(valor=Max('med_maximo'))
        .values('valor','month','day').order_by('month','day'))
    datos_diarios_min=list(Medicion.objects
        .filter(est_id=estacion)
        .filter(var_id=variable)
        .filter(med_fecha__year=periodo)
        .exclude(med_valor=0)
        .annotate(month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha'))
        .values('month','day')
        .annotate(valor=Min('med_minimo'))
        .values('valor','month','day').order_by('month','day'))

    med_avg=list(consulta.exclude(med_valor=0).annotate(c=Avg('med_valor')).values('c').order_by('month'))
    promedio = [d.get('c') for d in med_avg]
    maximo,maximo_dia = maximoshai(datos_diarios_max)
    minimo,minimo_dia = minimoshai(datos_diarios_min)
    for i in range(12):
        obj_hai=HumedadAire()
        obj_hai.est_id=obj_estacion
        obj_hai.hai_periodo=periodo
        obj_hai.hai_mes=i+1
        obj_hai.hai_maximo=maximo[i]
        obj_hai.hai_maximo_dia=maximo_dia[i]
        obj_hai.hai_minimo=minimo[i]
        obj_hai.hai_minimo_dia=minimo_dia[i]
        obj_hai.hai_promedio=promedio[i]
        datos.append(obj_hai)
    return datos
def maximoshai(datos_diarios_max):
    # retorna maxima humedad mensual y en que dia sucedio
    max_abs = []
    maxdia = []
    for i in range(1,13):
        val_max_abs=[]
        val_maxdia = []
        for fila in datos_diarios_max:
            if fila.get('month') == i:
                val_max_abs.append(fila.get('valor'))
                val_maxdia.append(fila.get('day'))
        max_abs.append(max(val_max_abs))
        maxdia.append(val_maxdia[val_max_abs.index(max(val_max_abs))])
    return max_abs,maxdia

def minimoshai(datos_diarios_min):
    # retorna minima humedad mensual y en que dia sucedio
    min_abs = []
    mindia = []
    for i in range(1,13):
        val_min_abs=[]
        val_mindia = []
        for fila in datos_diarios_min:
            if fila.get('month') == i:
                val_min_abs.append(fila.get('valor'))
                val_mindia.append(fila.get('day'))
        min_abs.append(min(val_min_abs))
        mindia.append(val_mindia[val_min_abs.index(min(val_min_abs))])
    return min_abs,mindia
