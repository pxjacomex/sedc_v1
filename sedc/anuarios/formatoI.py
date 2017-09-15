# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import TemperaturaAire
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)

def matrizI(estacion,variable,periodo):
    datos=[]
    consulta=Medicion.objects.filter(est_id=estacion).filter(var_id=variable).filter(med_fecha__year=periodo)
    if variable == 8:
        consulta = consulta.exclude(med_valor = 0, med_maximo = 0, med_minimo = 0)
    consulta=consulta.annotate(month=TruncMonth('med_fecha')).values('month')
    med_max=list(consulta.annotate(c=Max('med_valor')).values('c').order_by('month'))
    med_min=list(consulta.annotate(c=Min('med_valor')).values('c').order_by('month'))
    med_avg=list(consulta.annotate(c=Avg('med_valor')).values('c').order_by('month'))
    max_simple = [d.get('c') for d in med_max]
    min_simple = [d.get('c') for d in med_min]
    avg_simple = [d.get('c') for d in med_avg]
    return datos
