# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import PresionAtmosferica,HumedadSuelo,TemperaturaAgua,Caudal,NivelAgua
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)

def matrizI(estacion,variable,periodo):
    datos=[]
    obj_estacion=Estacion.objects.get(est_id=estacion)
    consulta=Medicion.objects.filter(est_id=estacion)\
    .filter(var_id=variable).filter(med_fecha__year=periodo)
    if variable == "8":
        consulta = consulta.exclude(med_valor = 0, med_maximo = 0, med_minimo = 0)
    consulta=consulta.annotate(month=TruncMonth('med_fecha')).values('month')
    med_max=list(consulta.annotate(c=Max('med_valor')).values('c').order_by('month'))
    med_min=list(consulta.annotate(c=Min('med_minimo')).values('c').order_by('month'))
    med_avg=list(consulta.annotate(c=Avg('med_valor')).values('c').order_by('month'))
    maximos = [d.get('c') for d in med_max]
    minimos = [d.get('c') for d in med_min]
    promedios = [d.get('c') for d in med_avg]
    if variable=="6":
        for i in range(len(promedios)):
            obj_hsu=HumedadSuelo()
            obj_hsu.est_id=obj_estacion
            obj_hsu.hsu_periodo=periodo
            obj_hsu.hsu_mes=i+1
            obj_hsu.hsu_maximo=maximos[i]
            obj_hsu.hsu_minimo=minimos[i]
            obj_hsu.hsu_promedio=promedios[i]
            datos.append(obj_hsu)
    elif variable=="8":
        for i in range(len(promedios)):
            obj_pat=PresionAtmosferica()
            obj_pat.est_id=obj_estacion
            obj_pat.pat_periodo=periodo
            obj_pat.pat_mes=i+1
            obj_pat.pat_maximo=maximos[i]
            obj_pat.pat_minimo=minimos[i]
            obj_pat.pat_promedio=promedios[i]
            datos.append(obj_pat)
    elif variable=="9":
        for i in range(len(promedios)):
            obj_tag=TemperaturaAgua()
            obj_tag.est_id=obj_estacion
            obj_tag.tag_periodo=periodo
            obj_tag.tag_mes=i+1
            obj_tag.tag_maximo=maximos[i]
            obj_tag.tag_minimo=minimos[i]
            obj_tag.tag_promedio=promedios[i]
            datos.append(obj_tag)
    elif variable=="10":
        for i in range(len(promedios)):
            obj_cau=Caudal()
            obj_cau.est_id=obj_estacion
            obj_cau.cau_periodo=periodo
            obj_cau.cau_mes=i+1
            obj_cau.cau_maximo=maximos[i]
            obj_cau.cau_minimo=minimos[i]
            obj_cau.cau_promedio=promedios[i]
            datos.append(obj_cau)
    elif variable=="11":
        for i in range(len(promedios)):
            obj_nag=NivelAgua()
            obj_nag.est_id=obj_estacion
            obj_nag.nag_periodo=periodo
            obj_nag.nag_mes=i+1
            obj_nag.nag_maximo=maximos[i]
            obj_nag.nag_minimo=minimos[i]
            obj_nag.nag_promedio=promedios[i]
            datos.append(obj_nag)
    return datos
