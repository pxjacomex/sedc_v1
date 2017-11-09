# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import RadiacionSolar
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count

from datetime import datetime

def matrizV(estacion,variable,periodo):
    #consulta=
    vel_media=list(Medicion.objects.filter(est_id=estacion).filter(var_id=4)
        .filter(med_fecha__year=periodo)
        .annotate(month=TruncMonth('med_fecha')).values('month')
        .annotate(c=Avg('med_valor')).values('c').order_by('month'))

    vel_media_simple = [d.get('c') for d in vel_media]
    vel_media_kmh = [x * int(3.6) for x in vel_media_simple]

    num_obs=list(Medicion.objects.filter(est_id=estacion).filter(var_id=4)
        .filter(med_fecha__year=periodo)
        .annotate(month=TruncMonth('med_fecha')).values('month')
        .annotate(obs=Count('med_valor')).values('obs')
        .order_by('month'))
    calma=list(Medicion.objects.filter(est_id=estacion).filter(var_id=4)
        .filter(med_fecha__year=periodo).filter(med_valor__lt=0.5)
        .annotate(month=TruncMonth('med_fecha')).values('month')
        .annotate(calma=Count('med_valor')).values('calma')
        .order_by('month'))
    datos_obs = [d.get('obs') for d in num_obs]
    datos_calma = [d.get('calma') for d in calma]
    dat_dvi=list(Medicion.objects
        .filter(est_id=estacion).filter(var_id=5)
        .filter(med_fecha__year=periodo)
        .values('med_valor','med_fecha').order_by('med_fecha','med_hora')
    )
    dat_vvi=list(Medicion.objects
        .filter(est_id=estacion).filter(var_id=4)
        .filter(med_fecha__year=periodo)
        .values('med_valor').order_by('med_fecha','med_hora')
    )
    dat_vvi_max=list(Medicion.objects
        .filter(est_id=estacion).filter(var_id=4)
        .filter(med_fecha__year=periodo)
        .values('med_maximo').order_by('med_fecha','med_hora')
    )
    valores=[[] for y in range(12)]
    direcciones=["N","NE","E","SE","S","SO","O","NO"]
    for mes in range(1,13):
        #crea una matriz en blanco
        vvi=[[0 for x in range(0)] for y in range(8)]
        vvi_max=[[0 for x in range(0)] for y in range(8)]
        for val_dvi,val_vvi,val_vvi_max in zip(dat_dvi,dat_vvi,dat_vvi_max):
            fecha=val_dvi.get('med_fecha')
            if fecha.month==mes:
            #agrupa las velocidades por direccion
                if val_vvi.get('med_valor') is not None:
                    if val_dvi.get('med_valor') < 22.5 or val_dvi.get('med_valor')>337.5:
                        vvi[0].append(val_vvi.get('med_valor'))
                        vvi_max[0].append(val_vvi_max.get('med_maximo'))
                    elif val_dvi.get('med_valor') < 67.5:
                        vvi[1].append(val_vvi.get('med_valor'))
                        vvi_max[1].append(val_vvi_max.get('med_maximo'))
                    elif val_dvi.get('med_valor') < 112.5:
                        vvi[2].append(val_vvi.get('med_valor'))
                        vvi_max[2].append(val_vvi_max.get('med_maximo'))
                    elif val_dvi.get('med_valor') < 157.5:
                        vvi[3].append(val_vvi.get('med_valor'))
                        vvi_max[3].append(val_vvi_max.get('med_maximo'))
                    elif val_dvi.get('med_valor') < 202.5:
                        vvi[4].append(val_vvi.get('med_valor'))
                        vvi_max[4].append(val_vvi_max.get('med_maximo'))
                    elif val_dvi.get('med_valor') < 247.5:
                        vvi[5].append(val_vvi.get('med_valor'))
                        vvi_max[5].append(val_vvi_max.get('med_maximo'))
                    elif val_dvi.get('med_valor') < 292.5:
                        vvi[6].append(val_vvi.get('med_valor'))
                        vvi_max[6].append(val_vvi_max.get('med_maximo'))
                    elif val_dvi.get('med_valor') < 337.5:
                        vvi[7].append(val_vvi.get('med_valor'))
                        vvi_max[7].append(val_vvi_max.get('med_maximo'))
                    dat_dvi.remove(val_dvi)
                    dat_vvi.remove(val_vvi)
                    dat_vvi_max.remove(val_vvi_max)
        maximos=[]
        valores[mes-1].append(mes)
        for j in range(8):
            #velocidades medias en esa direccion
            vel_med=float(sum(vvi[j])/len(vvi[j]))
            valores[mes-1].append(round(vel_med,2))
            #porcentaje en esa direccion
            por_med=float(len(vvi[j]))/datos_obs[mes-1]*100
            valores[mes-1].append(round(por_med,2))
            #maximos por direcciion
            if len(vvi_max[j])>0:
                maximos.append(max(vvi_max[j]))
            else:
                maximos.append(0)
        calma=round(float(datos_calma[mes-1])/datos_obs[mes-1]*100,2)
        valores[mes-1].append(calma)
        valores[mes-1].append(datos_obs[mes-1])
        valores[mes-1].append(round(max(maximos),2))
        valores[mes-1].append(direcciones[maximos.index(max(maximos))])
        valores[mes-1].append(vel_media_kmh[mes-1])
    return valores
