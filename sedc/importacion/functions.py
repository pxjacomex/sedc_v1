# -*- coding: utf-8 -*-
import json
from datetime import datetime,timedelta
from formato.models import Formato,Asociacion
from medicion.models import Medicion
from variable.models import Variable
from temporal.models import Datos
from datalogger.models import Datalogger
from formato.models import Clasificacion,Delimitador
from marca.models import Marca
datos=[]

#consultar formatos por datalogger y estacion
def consultar_formatos(marca):
    #asociacion=Asociacion.objects.filter(dat_id=datalogger).values()
    #lista=[item['for_id_id'] for item in asociacion]
    formatos=list(Formato.objects.filter(mar_id=marca).
        values('for_id','for_descripcion'))
    lista={}
    i=0
    for item in formatos:
        lista[item['for_id']]=item['for_descripcion']
    return lista
def construir_matriz(archivo,formato,estacion,request):
    cambiar_fecha=validar_datalogger(formato.mar_id_id)
    clasificacion=list(Clasificacion.objects.filter(
        for_id=formato.for_id).values())

    delimitador=Delimitador.objects.get(del_id=formato.del_id_id)

    i=0
    variables=[]
    request.session['for_id']=formato.for_id

    for fila in clasificacion:
        variable=Variable.objects.get(var_id=fila['var_id_id'])
        variables.append(variable)
    for linea in archivo.readlines():
        i+=1
        #controlar la fila de inicio
        if i>=formato.for_fil_ini:
            valores=linea.split(delimitador.del_caracter)
            fecha,hora=formato_fecha(formato,valores,cambiar_fecha)
            j=0
            for fila in clasificacion:
                #variable=Variable.objects.get(var_id=fila['var_id_id'])
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

                '''dato=Validacion(var_id=variables[j],est_id=estacion,
                    val_fecha=fecha,val_hora=hora,
                    val_valor=valor,val_maximo=maximo,val_minimo=minimo,
                    val_estado=True)'''
                dato=Datos(var_id=variables[j].var_id,est_id=estacion.est_id,
                    med_fecha=fecha,med_hora=hora,
                    med_valor=valor,med_maximo=maximo,med_minimo=minimo,
                    med_estado=True)
                #Validacion.objects.all().delete()
                datos.append(dato)
                j+=1
    return datos
#guardar la informacion
def guardar_datos(sobreescribir,request):
    print type(request.session['for_id'])
    if sobreescribir:
        eliminar_datos()
    #for valor in datos:
    #    valor.save()
    Datos.objects.bulk_create(datos)
    Datos.objects.all().delete()
    del datos[:]
#eliminar informacion en caso de sobreescribir
def eliminar_datos():
    fecha_ini=datos[0].med_fecha
    hora_ini=datos[0].med_hora
    fecha_fin=datos[-1].med_fecha
    hora_fin=datos[-1].med_hora
    Medicion.objects.filter(est_id=datos[0].est_id)\
    .filter(var_id=datos[0].var_id)\
    .filter(med_fecha__range=[fecha_ini,fecha_fin])\
    .filter(med_hora__range=[hora_ini,hora_fin]).delete()
#validar si son datalogger VAISALA para restar 5 horas
def validar_datalogger(marca):
    marca=Marca.objects.get(mar_id=marca)
    #asociacion=Asociacion.objects.filter(for_id=for_id).values()[0]
    #datalogger=Datalogger.objects.get(dat_id=asociacion['dat_id_id'])
    if marca.mar_nombre=='VAISALA':
        return True
    return False
#convertir fecha y hora al formato adecuado
def formato_fecha(formato,valores,cambiar_fecha):
    if formato.for_col_fecha==formato.for_col_hora:
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
