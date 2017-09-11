# -*- coding: utf-8 -*-
from validacion.models import Validacion
from frecuencia.models import Frecuencia
from medicion.models import Medicion
from estacion.models import Estacion
from datetime import datetime,timedelta,date
def generar_validacion(estacion):
    variables=list(Frecuencia.objects.filter(est_id=estacion).distinct('var_id'))
    obj_estacion=Estacion.objects.get(est_id=estacion)
    fecha_ini=""
    validaciones=[]
    for variable in variables:
        consulta=Validacion.objects.filter(est_id=estacion)\
        .filter(var_id=variable.var_id_id).order_by('-val_fecha')[:1]
        if consulta.exists():
            fecha_ini=consulta[0].val_fecha
        else:
            frecuencia=Frecuencia.objects.filter(est_id=estacion)\
            .filter(var_id=variable.var_id_id).order_by('fre_fecha_ini')[:1]
            #print frecuencia[0].fre_fecha_ini
            fecha_ini=frecuencia[0].fre_fecha_ini
        #fecha_ini=date(2017,1,1)
        mediciones=Medicion.objects.filter(est_id=estacion)\
        .filter(var_id=variable.var_id_id).order_by('-med_fecha')[:1]
        fecha_fin=mediciones[0].med_fecha
        print type(fecha_ini)
        print type(fecha_fin)
        fechas=list(Frecuencia.objects.filter(est_id=estacion)\
        .filter(var_id=variable.var_id_id).order_by('fre_fecha_ini'))
        i=0
        #frecuencia por defecto
        val_frecuencia=5
        rango=(fecha_fin-fecha_ini).days

        for item in range(1):
            print item
            val_fecha=fecha_ini+timedelta(days=item)
            if len(fechas)>1:
                if val_fecha>=fechas[i].get('fre_fecha_fin') and i<fechas.count():
                    i+=1
                val_frecuencia=fechas[i].fre_valor
            else:
                val_frecuencia=fechas[i].fre_valor
            val_num_dat=Medicion.objects.filter(est_id=estacion)\
            .filter(var_id=variable.var_id_id).filter(med_fecha=val_fecha).count()
            val_fre_reg=(60/val_frecuencia)*24
            val_porcentaje=float(val_num_dat)/val_fre_reg*100

            obj_validacion=Validacion(var_id=variable.var_id,est_id=obj_estacion,
            val_fecha=val_fecha,val_num_dat=val_num_dat,val_fre_reg=val_fre_reg,
            val_porcentaje=val_porcentaje)
            validaciones.append(obj_validacion)
            #obj_validacion.save()

    return validaciones








            #obj_val=Validacion(est_id=estacion,)
