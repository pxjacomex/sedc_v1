# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import TemperaturaAire
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)

def matrizIII(estacion,variable,periodo):
    datos=[]
    obj_estacion=Estacion.objects.get(est_id=estacion)
    med_avg=list(Medicion.objects.filter(est_id=estacion)
    .filter(var_id=variable).filter(med_fecha__year=periodo)
    .annotate(month=TruncMonth('med_fecha')).values('month')
    .annotate(c=Avg('med_valor')).values('c').order_by('month'))
    consulta_max=(Medicion.objects.filter(est_id=estacion)
        .filter(var_id=variable).filter(med_fecha__year=periodo)
        .exclude(med_maximo=None))
    if consulta_max.count()>0:
        datos_diarios_max=list(consulta_max.annotate(
        month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha'))
        .values('month','day').annotate(valor=Max('med_maximo'))
        .values('valor','month','day').order_by('month','day'))
    else:
        datos_diarios_max=list(Medicion.objects.filter(est_id=estacion)
            .filter(var_id=variable).filter(med_fecha__year=periodo)
            .annotate(month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha'))
            .values('month','day').annotate(valor=Max('med_valor'))
            .values('valor','month','day').order_by('month','day'))

    consulta_min=(Medicion.objects.filter(est_id=estacion)
        .filter(var_id=variable).filter(med_fecha__year=periodo)
        .exclude(med_minimo=None))
    if consulta_min.count()>0:
        datos_diarios_min=list(consulta_min.annotate(
        month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha'))
        .values('month','day').annotate(valor=Min('med_minimo'))
        .values('valor','month','day').order_by('month','day'))
    else:
        datos_diarios_min=list(Medicion.objects.filter(est_id=estacion)
            .filter(var_id=variable).filter(med_fecha__year=periodo)
            .exclude(med_valor=None)
            .annotate(month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha'))
            .values('month','day').annotate(valor=Min('med_valor'))
            .values('valor','month','day').order_by('month','day'))
    max_abs,max_dia,maximo = maximostai(datos_diarios_max)
    min_abs,min_dia,minimo = minimostai(datos_diarios_min)
    avg_simple = [d.get('c') for d in med_avg]
    for i in range(12):
        obj_tai=TemperaturaAire()
        obj_tai.est_id=obj_estacion
        obj_tai.tai_periodo=periodo
        obj_tai.tai_maximo_abs=max_abs[i]
        obj_tai.tai_maximo_dia=max_dia[i]
        obj_tai.tai_maximo=maximo[i]
        obj_tai.tai_minimo_abs=min_abs[i]
        obj_tai.tai_minimo_dia=min_dia[i]
        obj_tai.tai_minimo=minimo[i]
        obj_tai.tai_promedio=avg_simple[i]
        obj_tai.tai_mes=i+1
        datos.append(obj_tai)
    return datos

def maximostai(datos_diarios_max):
    # retorna maxima temp mensual y en que dia sucedio y media mensual de las maximas
    max_abs = []
    maxdia = []
    avgmax = []
    for i in range(1,13):
        val_max_abs=[]
        val_maxdia = []
        for fila in datos_diarios_max:
            if fila.get('month') == i:
                val_max_abs.append(fila.get('valor'))
                val_maxdia.append(fila.get('day'))
        max_abs.append(max(val_max_abs))
        maxdia.append(val_maxdia[val_max_abs.index(max(val_max_abs))])
        avgmax.append(sum(val_max_abs) / (len(val_max_abs)))
        #avgmax.append((len(val_max_abs)))
    return max_abs,maxdia, avgmax

def minimostai(datos_diarios_min):
    # retorna minima temp mensual y en que dia sucedio y media mensual de las minimas
    min_abs = []
    mindia = []
    avgmin = []
    for i in range(1,13):
        val_min_abs=[]
        val_mindia = []
        for fila in datos_diarios_min:
            if fila.get('month') == i:
                val_min_abs.append(fila.get('valor'))
                val_mindia.append(fila.get('day'))
        min_abs.append(min(val_min_abs))
        mindia.append(val_mindia[val_min_abs.index(min(val_min_abs))])
        avgmin.append(sum(val_min_abs) / (len(val_min_abs)))
        #avgmin.append((len(val_min_abs)))
    return min_abs,mindia,avgmin
