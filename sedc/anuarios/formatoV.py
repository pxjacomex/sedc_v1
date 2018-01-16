# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import Viento
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count

from datetime import datetime

def matrizV_mensual(estacion,variable,periodo):
    print "Inicio de la Función mensual ",datetime.now()
    #velocidad media en m/s
    vel_media=list(Medicion.objects.filter(est_id=estacion).filter(var_id=4)
        .filter(med_fecha__year=periodo)
        .annotate(month=TruncMonth('med_fecha')).values('month')
        .annotate(valor=Avg('med_valor')).values('valor').order_by('month'))
    #numero de registros por mes en velocidad
    num_obs=list(Medicion.objects.filter(est_id=estacion).filter(var_id=4)
        .filter(med_fecha__year=periodo)
        .annotate(month=TruncMonth('med_fecha')).values('month')
        .annotate(obs=Count('med_valor')).values('obs','month')
        .order_by('month'))
    #numero de registros mayores a 0.5 en velocidad
    calma=list(Medicion.objects.filter(est_id=estacion).filter(var_id=4)
        .filter(med_fecha__year=periodo).filter(med_valor__lt=0.5)
        .annotate(month=TruncMonth('med_fecha')).values('month')
        .annotate(calma=Count('med_valor')).values('calma')
        .order_by('month'))
    print "Inicio del For que recorrre los meses",datetime.now()
    direcciones=["N","NE","E","SE","S","SO","O","NO"]
    valores=[[] for y in range(12)]
    for item_obs,item_calma,item_velocidad in zip(num_obs,calma,vel_media):
        mes=item_obs.get('month').month
        print "Inicio de la consulta por mes",datetime.now()
        #lista de datos de la dirección de viento
        dat_dvi=list(Medicion.objects
            .filter(est_id=estacion).filter(var_id=5)
            .filter(med_fecha__year=periodo)
            .filter(med_fecha__month=mes)
            .values('med_valor','med_fecha').order_by('med_fecha','med_hora')
        )
        #lista de datos de velocidad del viento
        dat_vvi=list(Medicion.objects
            .filter(est_id=estacion).filter(var_id=4)
            .filter(med_fecha__year=periodo)
            .filter(med_fecha__month=mes)
            .values('med_valor','med_maximo').order_by('med_fecha','med_hora')
        )
        print "Fin de la consulta por mes",datetime.now()
        vvi=[[0 for x in range(0)] for y in range(8)]
        vvi_max=[[0 for x in range(0)] for y in range(8)]
        print "Clasificar velocididades por direccion",datetime.now()
        for val_dvi,val_vvi in zip(dat_dvi,dat_vvi):
            #agrupa las velocidades por direccion
            if val_vvi.get('med_valor') is not None:
                if val_dvi.get('med_valor') < 22.5 or val_dvi.get('med_valor')>337.5:
                    vvi[0].append(val_vvi.get('med_valor'))
                    vvi_max[0].append(val_vvi.get('med_valor')
                        if val_vvi.get('med_maximo') is None else
                        val_vvi.get('med_maximo'))
                elif val_dvi.get('med_valor') < 67.5:
                    vvi[1].append(val_vvi.get('med_valor'))
                    vvi_max[1].append(val_vvi.get('med_valor')
                        if val_vvi.get('med_maximo') is None else
                        val_vvi.get('med_maximo'))
                elif val_dvi.get('med_valor') < 112.5:
                    vvi[2].append(val_vvi.get('med_valor'))
                    vvi_max[2].append(val_vvi.get('med_valor')
                        if val_vvi.get('med_maximo') is None else
                        val_vvi.get('med_maximo'))
                elif val_dvi.get('med_valor') < 157.5:
                    vvi[3].append(val_vvi.get('med_valor'))
                    vvi_max[3].append(val_vvi.get('med_valor')
                        if val_vvi.get('med_maximo') is None else
                        val_vvi.get('med_maximo'))
                elif val_dvi.get('med_valor') < 202.5:
                    vvi[4].append(val_vvi.get('med_valor'))
                    vvi_max[4].append(val_vvi.get('med_valor')
                        if val_vvi.get('med_maximo') is None else
                        val_vvi.get('med_maximo'))
                elif val_dvi.get('med_valor') < 247.5:
                    vvi[5].append(val_vvi.get('med_valor'))
                    vvi_max[5].append(val_vvi.get('med_valor')
                        if val_vvi.get('med_maximo') is None else
                        val_vvi.get('med_maximo'))
                elif val_dvi.get('med_valor') < 292.5:
                    vvi[6].append(val_vvi.get('med_valor'))
                    vvi_max[6].append(val_vvi.get('med_valor')
                        if val_vvi.get('med_maximo') is None else
                        val_vvi.get('med_maximo'))
                elif val_dvi.get('med_valor') < 337.5:
                    vvi[7].append(val_vvi.get('med_valor'))
                    vvi_max[7].append(val_vvi.get('med_valor')
                        if val_vvi.get('med_maximo') is None else
                        val_vvi.get('med_maximo'))
        print "Fin de la clasificacion",datetime.now()
        maximos=[]
        valores[mes-1].append(mes)
        #recorro la matriz de datos en base al número de direcciones
        for j in range(8):
            if len(vvi[j])>0:
                vel_med=float(sum(vvi[j])/len(vvi[j]))
                por_med=float(len(vvi[j]))/item_obs.get('obs')*100
            else:
                vel_med=0.0
                por_med=0.0
            #promedio de velocidades medias por direccion
            valores[mes-1].append(round(vel_med,2))
            #porcentaje por direccion
            valores[mes-1].append(round(por_med,2))
            #maximos por direcciion
            if len(vvi_max[j])>0:
                maximos.append(max(vvi_max[j]))
            else:
                maximos.append(float(0))
        valor_calma=round(float(item_calma.get('calma'))/item_obs.get('obs')*100,2)
        valores[mes-1].append(valor_calma)
        valores[mes-1].append(item_obs.get('obs'))
        valores[mes-1].append(round(max(maximos),2))
        valores[mes-1].append(direcciones[maximos.index(max(maximos))])
        valores[mes-1].append(round(item_velocidad.get('valor'),2))
    return valores


def datos_viento(datos,estacion,periodo):
    lista=[]
    obj_estacion=Estacion.objects.get(est_id=estacion)
    for fila in datos:
        if len(fila)>0:
            obj_viento=Viento()
            obj_viento.est_id=obj_estacion
            obj_viento.vie_periodo=periodo
            obj_viento.vie_mes=fila[0]
            obj_viento.vie_vel_N=fila[1]
            obj_viento.vie_por_N=fila[2]
            obj_viento.vie_vel_NE=fila[3]
            obj_viento.vie_por_NE=fila[4]
            obj_viento.vie_vel_E=fila[5]
            obj_viento.vie_por_E=fila[6]
            obj_viento.vie_vel_SE=fila[7]
            obj_viento.vie_por_SE=fila[8]
            obj_viento.vie_vel_S=fila[9]
            obj_viento.vie_por_S=fila[10]
            obj_viento.vie_vel_SO=fila[11]
            obj_viento.vie_por_SO=fila[12]
            obj_viento.vie_vel_O=fila[13]
            obj_viento.vie_por_O=fila[14]
            obj_viento.vie_vel_NO=fila[15]
            obj_viento.vie_por_NO=fila[16]
            obj_viento.vie_calma=fila[17]
            obj_viento.vie_obs=fila[18]
            obj_viento.vie_vel_max=fila[19]
            obj_viento.vie_vel_dir=fila[20]
            obj_viento.vie_vel_med=fila[21]
            lista.append(obj_viento)
    return lista
