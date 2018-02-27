# -*- coding: utf-8 -*-
import json
import sys
from datetime import datetime,timedelta
from estacion.models import Estacion
from medicion.models import Medicion
from variable.models import Variable
from temporal.models import Datos
from datalogger.models import Datalogger
from vacios.models import Vacios
from formato.models import Clasificacion,Delimitador,Formato,Asociacion,Fecha,Hora
from marca.models import Marca
from importacion.forms import VaciosForm
from django.core.serializers import serialize,deserialize
from django.db import connection


#consultar formatos por datalogger y estacion
def consultar_formatos(marca):
    formatos=list(Formato.objects.filter(mar_id=marca).
        values('for_id','for_descripcion'))
    lista={}
    i=0
    for item in formatos:
        lista[item['for_id']]=item['for_descripcion']
    return lista
#leer el archivo
def procesar_archivo(archivo,form,request):
    #try:
    formato=form.cleaned_data['formato']
    estacion=form.cleaned_data['estacion']
    datalogger=form.cleaned_data['datalogger']
    sobreescribir=form.cleaned_data['sobreescribir']
    datos,variables=construir_matriz(archivo,formato,estacion,datalogger)
    valid=validar_fechas(datos)
    vacio=verificar_vacios(datos)
    message=str("")
    datos_json=serialize('json', datos)
    request.session['datos']=datos_json
    request.session['sobreescribir']=sobreescribir
    request.session['variables']=serialize('json',variables)

    if vacio:
        request.session['vacios']=serialize('json',objetos_vacios(datos,variables))
        #lista_vacios=objetos_vacios(datos,variables)
    if not valid and not sobreescribir:
        message="Datos existentes, por favor seleccione la opcion sobreescribir"
    elif not valid and sobreescribir:
        message="Se va a sobreescribir la informacion"
    elif valid and sobreescribir:
        message="Los datos no existen, no hay que sobreescribir la información"
    else:
        message="Ninguno"
    context={
        'variables':informacion_archivo(formato),
        'fechas':rango_fecha(datos),
        'message':message,
        'valid':valid,
        'vacio':vacio,
    }
    '''except ValueError:
        context={
            'message':"El formato del datalogger no coincide con el archivo",
            'valid':False
        }
        '''
    return context
def procesar_archivo_automatico(archivo,formato,estacion,datalogger):
    datos,variables=construir_matriz(archivo,formato,estacion,datalogger)
    return datos,variables

#leer el archivo y convertirlo a una matriz de objetos de la clase Datos
def construir_matriz(archivo,formato,estacion,datalogger):
    #variables para el acumulado
    ValorReal = 0
    UltimoValor = 0
    #determinar si debemos restar 5 horas a la fecha del archivo
    cambiar_fecha=validar_datalogger(formato.mar_id)
    #validar si los valores del archivo son acumulados
    acumulado=validar_acumulado(formato.mar_id)
    clasificacion=list(Clasificacion.objects.filter(
        for_id=formato.for_id).values())
    i=0
    variables=[]
    datos=[]
    for fila in clasificacion:
        variable=Variable.objects.get(var_id=fila['var_id_id'])
        variables.append(variable)
    for linea in archivo.readlines():
        i+=1
        #controlar la fila de inicio
        if i>=formato.for_fil_ini:
            valores=linea.split(formato.del_id.del_caracter)
            fecha=formato_fecha(formato,valores,cambiar_fecha)
            j=0
            for fila in clasificacion:
                #variable=Variable.objects.get(var_id=fila['var_id_id'])
                if fila['cla_valor'] is not None:
                    valor=float(valores[fila['cla_valor']])
                    if acumulado:
                        dblValor=valor
                        if dblValor==0:
                            UltimoValor=0
                        ValorReal=dblValor-UltimoValor
                        if ValorReal<0:
                            ValorReal=dblValor
                        UltimoValor=dblValor
                        valor=ValorReal
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
                dato=Datos(var_id=variables[j].var_id,est_id=estacion.est_id,
                    med_fecha=fecha,mar_id=datalogger.mar_id,
                    med_valor=valor,med_maximo=maximo,med_minimo=minimo,
                    med_estado=True)
                datos.append(dato)
                j+=1
            if formato.for_tipo=='automatico':
                formato.for_fil_ini=i+1
                formato.save()
    return datos,variables
#verficar vacios
def verificar_vacios(datos):
    estado=False
    vacios=[]
    fecha_archivo=datos[0].med_fecha.date()
    medicion=Medicion.objects.filter(est_id=datos[0].est_id)\
    .filter(var_id=datos[0].var_id).values('med_fecha').reverse()[:1]
    if len(medicion)>0:
        fecha_datos=list(medicion)[0].get('med_fecha').date()
        intervalo=timedelta(days=1)
        fecha_comparacion=fecha_datos+intervalo

        if fecha_comparacion>=fecha_archivo:
            estado=False
        else:
            estado=True
    else:
        estado=False
    return estado
def objetos_vacios(datos,variables):
    lista_vacios=[]
    medicion=Medicion.objects.filter(est_id=datos[0].est_id)\
    .filter(var_id=datos[0].var_id).values('med_fecha').reverse()[:1]
    fecha_datos=list(medicion)[0].get('med_fecha').date()
    hora_datos=list(medicion)[0].get('med_fecha').time()
    estacion=Estacion.objects.get(est_id=datos[0].est_id)
    for variable in variables:
        vacio=Vacios()
        vacio.est_id=estacion
        vacio.var_id=variable
        vacio.vac_fecha_ini=fecha_datos
        vacio.vac_hora_ini=hora_datos
        vacio.vac_fecha_fin=datos[0].med_fecha.date()
        vacio.vac_hora_fin=datos[0].med_fecha.time()
        lista_vacios.append(vacio)
    return lista_vacios

#guardar la informacion
def guardar_datos(request):
    sobreescribir=request.session['sobreescribir']
    datos_json=request.session['datos']
    datos=[]
    variables=[]
    for obj_dato in deserialize("json",datos_json):
        datos.append(obj_dato.object)
    for obj_variable in deserialize("json",request.session['variables']):
        variables.append(obj_variable.object.pk)
    if sobreescribir:
        eliminar_datos(datos,variables)
    Datos.objects.bulk_create(datos)
    Datos.objects.all().delete()
    del datos[:]
def guardar_datos_automatico(datos,variables):
    list_var=[]
    for variable in variables:
        list_var.append(variable.var_id)
    eliminar_datos(datos,list_var)
    Datos.objects.bulk_create(datos)
    Datos.objects.all().delete()
    del datos[:]

#eliminar informacion en caso de sobreescribir
def eliminar_datos(datos,variables):
    fecha_ini=datos[0].med_fecha
    fecha_fin=datos[-1].med_fecha
    fec_ini=str(fecha_ini)
    fec_fin=str(fecha_fin)
    for var_id in variables:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM medicion_medicion \
            WHERE est_id_id=%s\
            and var_id_id=%s and med_fecha>=%s \
            and med_fecha<=%s",
            [datos[0].est_id,var_id,fec_ini,fec_fin] )
#guardar el registro de los Vacios
def guardar_vacios(request,observacion):
    vacios_json=request.session['vacios']
    for obj_vacio in deserialize("json",vacios_json):
        obj_vacio.object.vac_observacion=observacion
        obj_vacio.save()
#validar si son datalogger VAISALA para restar 5 horas
def validar_datalogger(marca):
    #marca=Marca.objects.get(mar_id=marca)
    print marca.mar_nombre
    if marca.mar_nombre=='VAISALA':
        return True
    return False
def validar_acumulado(marca):
    #marca=Marca.objects.get(mar_id=marca)
    if marca.mar_nombre=='HOBO':
        return True
    return False

#convertir fecha y hora al formato adecuado
def formato_fecha(formato,valores,cambiar_fecha):
    if formato.for_col_fecha==formato.for_col_hora:
        separar=valores[formato.for_col_fecha].split(" ")
        fecha_str=separar[0]
        hora_str=separar[1]
    else:
        fecha_str=valores[formato.for_col_fecha]
        hora_str=valores[formato.for_col_hora]
    fecha_str=fecha_str.strip('\"')
    hora_str=hora_str.strip('\"')
    try:
        fecha=datetime.strptime(fecha_str,formato.fec_id.fec_codigo)
    except ValueError:
        fecha=cambiar_formato_fecha(formato,fecha_str)
    try:
        hora=datetime.strptime(hora_str,formato.hor_id.hor_codigo)
    except ValueError:
        hora=cambiar_formato_hora(formato,hora_str)
    fecha_hora=datetime(fecha.year,fecha.month,fecha.day,hora.hour,hora.minute,hora.second)
    if cambiar_fecha:
        intervalo=timedelta(hours=5)
        fecha_hora-=intervalo
    return fecha_hora
def cambiar_formato_fecha(formato,fecha_str):
    con_fecha=list(Fecha.objects.exclude(fec_id=formato.fec_id.fec_id))
    for fila in con_fecha:
        try:
            fecha=datetime.strptime(fecha_str,fila.fec_codigo)
            formato.fec_id=fila
            formato.save()
            break
        except ValueError:
            pass
    return fecha
#busca un formato de hora para registro del archivo
def cambiar_formato_hora(formato,hora_str):
    con_hora=list(Hora.objects.exclude(hor_id=formato.hor_id.hor_id))
    for fila in con_hora:
        try:
            hora=datetime.strptime(hora_str,fila.hor_codigo)
            formato.hor_id=fila
            formato.save()
            break
        except ValueError:
            pass
    return hora


# Poner en una variable la información de las variables a importar
def informacion_archivo(formato):
    clasificacion=list(Clasificacion.objects.filter(
        for_id=formato.for_id).values())
    i=1
    cadena=""
    for fila in clasificacion:
        variable=Variable.objects.get(var_id=fila['var_id_id'])
        if i<len(clasificacion):
            cadena+=variable.var_nombre+","
        else:
            cadena+=variable.var_nombre
        i+=1
    return cadena
#Información del rango de fechas a importar
def rango_fecha(datos):
    fecha_ini=datos[0].med_fecha
    fecha_fin=datos[-1].med_fecha
    cadena=str(fecha_ini)+" al "+ str(fecha_fin)
    return cadena
#verificar los datos del archivo
def validar_fechas(datos):
    fecha_ini=datos[0].med_fecha
    #hora_ini=datos[0].med_hora
    fecha_fin=datos[-1].med_fecha
    #hora_fin=datos[-1].med_hora
    fec_ini=str(fecha_ini)
    fec_fin=str(fecha_fin)
    consulta=list(Medicion.objects.raw(
        'SELECT med_id\
        FROM  medicion_medicion WHERE med_fecha>=%s \
        and med_fecha<=%s and est_id_id=%s\
        and var_id_id=%s',
        [fec_ini,fec_fin,datos[0].est_id,datos[0].var_id]
        )
    )
    if len(consulta)>0:
        return False
    return True
def validar_fechas_archivo(archivo,formato,estacion):
    cambiar_fecha=validar_datalogger(formato.mar_id)
    i=0
    datos=archivo.readlines()
    for linea in datos:
        i+=1
        #controlar la fila de inicio
        if i==formato.for_fil_ini:
            valores_ini=linea.split(formato.del_id.del_caracter)
            fecha_ini=formato_fecha(formato,valores_ini,cambiar_fecha)
        if i==len(datos):
            valores_fin=linea.split(formato.del_id.del_caracter)
            fecha_fin=formato_fecha(formato,valores_fin,cambiar_fecha)
    consulta=(Medicion.objects.filter(est_id=estacion)
        .filter(med_fecha__range=[fecha_ini,fecha_fin])).exists()

    archivo.seek(0,0)
    return consulta
    '''archivo.seek(0)
    linea_fin=archivo.readline()
    valores_fin=linea_fin.split(formato.del_id.del_caracter)
    fecha_fin=formato_fecha(formato,valores_fin,cambiar_fecha)
    print fecha_fin'''
