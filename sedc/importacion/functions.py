# -*- coding: utf-8 -*-
import json
from datetime import datetime,timedelta
from formato.models import Formato,Asociacion
from validacion.models import Validacion
from variable.models import Variable
from datalogger.models import Datalogger
from formato.models import Clasificacion,Delimitador
#consultar formatos por datalogger y estacion
def consultar_formatos(datalogger):
    asociacion=Asociacion.objects.filter(dat_id=datalogger).values()
    lista=[item['for_id_id'] for item in asociacion]
    formatos=list(Formato.objects.filter(for_id__in=lista).
        values('for_id','for_descripcion'))
    datos={}
    i=0
    for item in formatos:
        datos[item['for_id']]=item['for_descripcion']
    return datos
def construir_matriz(archivo,formato,estacion):
    cambiar_fecha=validar_datalogger(formato.for_id)
    clasificacion=list(Clasificacion.objects.filter(
        for_id=formato.for_id).values())
    delimitador=Delimitador.objects.get(del_id=formato.del_id_id)
    datos=[]
    i=0
    for linea in archivo.readlines():
        i+=1
        #controlar la fila de inicio
        if i>=formato.for_fil_ini:
            valores=linea.split(delimitador.del_caracter)
            fecha,hora=formato_fecha(formato,valores,cambiar_fecha)
            for fila in clasificacion:
                variable=Variable.objects.get(var_id=fila['var_id_id'])
                if fila['cla_valor'] is not None:
                    valor=float(valores[fila['cla_valor']])
                else:
                    valor=None
                if fila['cla_maximo'] is not None:
                    maximo=float(valores[fila['cla_maximo']])
                else:
                    maximo=None
                if fila['cla_minimo'] is not None:
                    minimo=float(valores[fila['cla_minimo']])
                else:
                    minimo=None
                print estacion.est_id,variable,fecha,hora,valor,maximo,minimo
                dato=Validacion(var_id=variable,est_id=estacion,
                    val_fecha=fecha,val_hora=hora,
                    val_valor=valor,val_maximo=maximo,val_minimo=minimo,
                    val_estado=True)
                #med.save()
                #Validacion.objects.all().delete()
                datos.append(dato)
    return datos
#validar si son datalogger VAISALA para restar 5 horas
def validar_datalogger(for_id):
    asociacion=Asociacion.objects.filter(for_id=for_id).values()[0]
    print asociacion
    datalogger=Datalogger.objects.get(dat_id=asociacion['dat_id_id'])
    if datalogger.dat_marca=='VAISALA':
        return True
    return False
#convertir fecha y hora al formato adecuado
def formato_fecha(formato,valores,cambiar_fecha):
    if formato.for_col_hora==formato.for_col_hora:
        fecha_hora=datetime.strptime(valores[formato.for_col_hora],
            formato.for_fecha+str(" ")+formato.for_hora)
    else:
        fecha_hora=datetime.strptime(valores[formato.for_col_fecha]+
            valores[formato.for_col_hora],formato.for_fecha+str(" ")+
            formato.for_hora)
    #fecha_hora=validar_datalogger(formato.for_id,fecha_hora)
    if cambiar_fecha:
        intervalo=timedelta(hours=5)
        fecha_hora-=intervalo
    fecha=fecha_hora.strftime('%Y-%m-%d')
    hora=fecha_hora.strftime('%H:%M:%S')
    return fecha,hora
