# -*- coding: utf-8 -*-
from estacion.models import Estacion
from variable.models import Variable, Unidad
from medicion.models import Medicion
from django.db.models import Max, Min, Avg, Count,Sum
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)
import plotly.offline as opy
import plotly.graph_objs as go
import datetime, calendar
from datetime import timedelta
from django.db import connection
import time

def grafico(form):
    print time.ctime()
    estacion=form.cleaned_data['estacion']
    variable=form.cleaned_data['variable']
    fecha_inicio=form.cleaned_data['inicio']
    fecha_fin=form.cleaned_data['fin']
    frecuencia=form.cleaned_data['frecuencia']
    div=""
    #frecuencia instantanea
    if(frecuencia==str(0)):
        valores,maximos,minimos,tiempo=datos_instantaneos(estacion,variable,fecha_inicio,fecha_fin)
    #frecuencia 5 minutos
    elif(form.cleaned_data['frecuencia']==str(1)):
        valores,maximos,minimos,tiempo=datos_5minutos(estacion,variable,fecha_inicio,fecha_fin)
    #frecuencia horaria
    #elif(form.cleaned_data['frecuencia']==str(2)):

    #frecuencia diaria
    #elif(form.cleaned_data['frecuencia']==str(3)):

    #frecuencia mensual
    #elif(form.cleaned_data['frecuencia']==str(4)):

    else:
        valores,maximos,minimos,tiempo=datos_instantaneos(estacion,variable,fecha_inicio,fecha_fin)
    if len(valores)>0:
        print "llego"
        trace0 = go.Scatter(
            x = tiempo,
            y = maximos,
            name = 'Max',
            mode = 'lines',
            line = dict(
                color = ('rgb(205, 12, 24)'),
                )
        )
        trace1 = go.Scatter(
            x = tiempo,
            y = minimos,
            name = 'Min',
            mode = 'lines',
            line = dict(
                color = ('rgb(50, 205, 50)'),
                )
        )
        trace2 = go.Scatter(
            x = tiempo,
            y = valores,
            name = 'Media',
            mode = 'lines',
            line = dict(
                color = ('rgb(22, 96, 167)'),
                )
        )
        data = go.Data([trace0,trace1,trace2])
        layout = go.Layout(
            title = variable.var_nombre +\
            " " + str(titulo_frecuencia(frecuencia))+\
            " " + estacion.est_codigo,
            yaxis = dict(title = variable.var_nombre + \
                         str(" (") + titulo_unidad(variable)+ str(")")),
            #xaxis = dict(range = [str(fecha_inicio),str(fecha_fin)])
            )
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
    return div
def datos_instantaneos(estacion,variable,fecha_inicio,fecha_fin):
    year_ini=fecha_inicio.strftime('%Y')
    year_fin=fecha_fin.strftime('%Y')
    var_cod=variable.var_codigo
    if year_ini==year_fin:
        tabla=var_cod+'.m'+year_ini
        sql='SELECT * FROM '+tabla+ ' WHERE '
        sql+='est_id_id='+str(estacion.est_id)+ ' and '
        sql+='med_fecha>=\''+str(fecha_inicio)+'\' and '
        sql+='med_fecha<=\''+str(fecha_fin)+'\' order by med_fecha'
        consulta=list(Medicion.objects.raw(sql))
    else:
        range_year=range(int(year_ini),int(year_fin)+1)
        consulta=[]
        for year in range_year:
            tabla=var_cod+'.m'+str(year)
            if str(year)==year_ini:
                sql='SELECT * FROM '+tabla+ ' WHERE '
                sql+='est_id_id='+str(estacion.est_id)+ ' and '
                sql+='med_fecha>=\''+str(fecha_inicio)+'\' order by med_fecha'
            elif str(year)==year_fin:
                sql='SELECT * FROM '+tabla+ ' WHERE '
                sql+='est_id_id='+str(estacion.est_id)+ ' and '
                sql+='med_fecha<=\''+str(fecha_fin)+' 23:59:59 \' order by med_fecha'
            else:
                sql='SELECT * FROM '+tabla+ ' WHERE '
                sql+='est_id_id='+str(estacion.est_id)+' order by med_fecha'
            consulta.extend(list(Medicion.objects.raw(sql)))
    valor=[]
    maximo=[]
    minimo=[]
    frecuencia=[]
    for fila in consulta:
        if fila.med_valor is not None:
            valor.append(fila.med_valor)
        else:
            valor.append(None)
        if fila.med_maximo is not None:
            maximo.append(fila.med_maximo)
        else:
            maximo.append(None)
        if fila.med_minimo is not None:
            minimo.append(fila.med_minimo)
        else:
            minimo.append(None)
        #frecuencia.append(datetime.datetime.combine(fila['med_fecha'],fila['med_hora']))
        frecuencia.append(fila.med_fecha)
    return valor,maximo,minimo,frecuencia
def datos_5minutos(estacion,variable,fecha_inicio,fecha_fin):
    year_ini=fecha_inicio.strftime('%Y')
    year_fin=fecha_fin.strftime('%Y')
    var_cod=variable.var_codigo
    cursor = connection.cursor()
    if year_ini==year_fin:
        tabla=var_cod+'.m'+year_ini
        if variable.var_id==1:
            sql='SELECT sum(med_valor) as valor, '
            sql+='to_timestamp(floor((extract(\'epoch\' '
            sql+='from med_fecha) / 300 )) * 300)'
            sql+='AT TIME ZONE \'UTC5\' as interval_alias '
            sql+='FROM '+tabla+ ' WHERE '
            sql+='est_id_id='+str(estacion.est_id)+ ' and '
            sql+='med_fecha>=\''+str(fecha_inicio)+'\' and '
            sql+='med_fecha<=\''+str(fecha_fin)+'\''
            sql+='GROUP BY interval_alias '
            sql+='ORDER BY interval_alias'
        else:
            sql='SELECT avg(med_valor) as valor, '
            sql+='to_timestamp(floor((extract(\'epoch\' '
            sql+='from med_fecha) / 300 )) * 300)'
            sql+='AT TIME ZONE \'UTC5\' as interval_alias '
            sql+='FROM '+tabla+ ' WHERE '
            sql+='est_id_id='+str(estacion.est_id)+ ' and '
            sql+='med_fecha>=\''+str(fecha_inicio)+'\' and '
            sql+='med_fecha<=\''+str(fecha_fin)+'\' 23:59:59'
            sql+='GROUP BY interval_alias '
            sql+='ORDER BY interval_alias'
        cursor.execute(sql)
    else:
        range_year=range(int(year_ini),int(year_fin)+1)
        consulta=[]
        for year in range_year:
            tabla=var_cod+'.m'+str(year)
            if str(year)==year_ini:
                sql='SELECT * FROM '+tabla+ ' WHERE '
                sql+='est_id_id='+str(estacion.est_id)+ ' and '
                sql+='med_fecha>=\''+str(fecha_inicio)+'\' order by med_fecha'
            elif str(year)==year_fin:
                sql='SELECT * FROM '+tabla+ ' WHERE '
                sql+='est_id_id='+str(estacion.est_id)+ ' and '
                sql+='med_fecha<=\''+str(fecha_fin)+' 23:59:59 \' order by med_fecha'
            else:
                sql='SELECT * FROM '+tabla+ ' WHERE '
                sql+='est_id_id='+str(estacion.est_id)+' order by med_fecha'
            consulta.extend(list(Medicion.objects.raw(sql)))
    datos=dictfetchall(cursor)
    valor=[]
    maximo=[]
    minimo=[]
    frecuencia=[]
    intervalo=timedelta(minutes=5)
    fecha=datetime.datetime.combine(fecha_inicio, datetime.datetime.min.time())
    for fila in datos:
        fecha_datos=fila.get('interval_alias')
        #print "fechadatos",fecha_datos
        while True:
            if fecha_datos==fecha:
                valor.append(fila.get('valor'))
                maximo.append(fila.get('maximo'))
                minimo.append(fila.get('minimo'))
                frecuencia.append(fila.get('interval_alias'))
                fecha+=intervalo
                break
            else:
                valor.append(0)
                maximo.append(None)
                minimo.append(None)
                frecuencia.append(fecha)

                fecha+=intervalo
                #print "fecha",fecha
        '''valor.append(fila.get('valor'))
        maximo.append(fila.get('maximo'))
        minimo.append(fila.get('minimo'))
        frecuencia.append(fila.get('interval_alias'))'''
    cursor.close()
    for tim,val in zip(frecuencia,valor):
        print tim,val
    return valor,maximo,minimo,frecuencia


def datos_horarios(consulta,variable):
    consulta=consulta.annotate(year=ExtractYear('med_fecha'),
        month=ExtractMonth('med_fecha'),
        day=ExtractDay('med_fecha'),
        hour=ExtractHour('med_fecha')
    ).values('year','month','day','hour')
    if(variable.var_id==1):
        consulta=list(consulta.annotate(valor=Sum('med_valor')).
        values('valor','year','month','day','hour').
        order_by('year','month','day','hour'))
    else:
        consulta=list(consulta.annotate(valor=Avg('med_valor'),
        maximo=Max('med_maximo'),minimo=Min('med_minimo')).
        values('valor','maximo','minimo','year','month','day','hour').
        order_by('year','month','day','hour'))
    valor=[]
    maximo=[]
    minimo=[]
    frecuencia=[]
    for fila in consulta:
        if fila.get('valor') is not None:
            valor.append(fila.get('valor'))
        if fila.get('maximo') is not None:
            maximo.append(fila.get('maximo'))
        if fila.get('minimo') is not None:
            minimo.append(fila.get('minimo'))
        fecha_str = (str(fila.get('year'))+":"+
            str(fila.get('month'))+":"+str(fila.get('day')))
        fecha = datetime.datetime.strptime(fecha_str,'%Y:%m:%d').date()
        hora=datetime.time(fila.get('hour'))
        fecha_hora=datetime.datetime.combine(fecha,hora)
        frecuencia.append(fecha_hora)
    return valor,maximo,minimo,frecuencia
def datos_diarios(consulta,variable):
    consulta=consulta.annotate(
        year=ExtractYear('med_fecha'),
        month=ExtractMonth('med_fecha'),
        day=ExtractDay('med_fecha')
    ).values('year','month','day')
    if(variable.var_id==1):
        consulta=list(consulta.annotate(valor=Sum('med_valor')).
        values('valor','year','month','day').
        order_by('year','month','day'))
    else:
        consulta=list(consulta.annotate(valor=Avg('med_valor'),
        maximo=Max('med_maximo'),minimo=Min('med_minimo')).
        values('valor','maximo','minimo','year','month','day').
        order_by('year','month','day'))
    valor=[]
    maximo=[]
    minimo=[]
    frecuencia=[]
    for fila in consulta:
        if fila.get('valor') is not None:
            valor.append(fila.get('valor'))
        if fila.get('maximo') is not None:
            maximo.append(fila.get('maximo'))
        if fila.get('minimo') is not None:
            minimo.append(fila.get('minimo'))
        fecha_str = (str(fila.get('year'))+":"+
            str(fila.get('month'))+":"+str(fila.get('day')))
        fecha = datetime.datetime.strptime(fecha_str,'%Y:%m:%d').date()
        frecuencia.append(fecha)
    return valor,maximo,minimo,frecuencia
def datos_mensuales(consulta,variable):
    consulta=consulta.annotate(
        year=ExtractYear('med_fecha'),
        month=ExtractMonth('med_fecha')
    ).values('month','year')
    if(variable.var_id==1):
        consulta=list(consulta.annotate(valor=Sum('med_valor')).
        values('valor','month','year').
        order_by('year','month'))
    else:
        consulta=list(consulta.annotate(valor=Avg('med_valor'),
        maximo=Max('med_maximo'),minimo=Min('med_minimo')).
        values('valor','maximo','minimo','month','year').
        order_by('year','month'))
    valor=[]
    maximo=[]
    minimo=[]
    frecuencia=[]
    for fila in consulta:
        if fila.get('valor') is not None:
            valor.append(fila.get('valor'))
        if fila.get('maximo') is not None:
            maximo.append(fila.get('maximo'))
        if fila.get('minimo') is not None:
            minimo.append(fila.get('minimo'))
        fecha_str = str(calendar.month_abbr[fila.get('month')])+" "+str(fila.get('year'))
        frecuencia.append(fecha_str)
    return valor,maximo,minimo,frecuencia
def titulo_unidad(variable):
    uni=list(Unidad.objects.filter(uni_id=variable.uni_id.uni_id).values())
    return uni[0].get('uni_sigla')

def titulo_frecuencia(frecuencia):
    nombre = []
    if frecuencia == '0':
        nombre = 'Instantanea'
    if frecuencia == '1':
        nombre = '5 Minutos'
    elif frecuencia == '2':
        nombre = 'Horaria'
    elif frecuencia == '3':
        nombre = 'Diaria'
    elif frecuencia == '4':
        nombre = 'Mensual'
    return nombre

def dictfetchall(cursor):
    #Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def datos_horarios_json(est_id,var_id,fec_ini,fec_fin):
    consulta=(Medicion.objects.filter(est_id=est_id)
    .filter(var_id=var_id).filter(med_fecha__range=[fec_ini,fec_fin]))
    consulta=consulta.annotate(year=ExtractYear('med_fecha'),
        month=ExtractMonth('med_fecha'),
        day=ExtractDay('med_fecha'),
        hour=ExtractHour('med_fecha')
    ).values('year','month','day','hour')
    if(var_id==1):
        consulta=list(consulta.annotate(valor=Sum('med_valor')).
        values('valor','year','month','day','hour').
        order_by('year','month','day','hour'))
    else:
        consulta=list(consulta.annotate(valor=Avg('med_valor'),
        maximo=Max('med_maximo'),minimo=Min('med_minimo')).
        values('valor','maximo','minimo','year','month','day','hour').
        order_by('year','month','day','hour'))
    datos=[]
    if len(consulta)>0:
        for fila in consulta:
            fecha_str = (str(fila.get('year'))+":"+
                str(fila.get('month'))+":"+str(fila.get('day')))
            print fecha_str
            fecha = datetime.datetime.strptime(fecha_str,'%Y:%m:%d').date()
            hora=datetime.time(fila.get('hour'))
            fecha_hora=datetime.datetime.combine(fecha,hora)
            dato={
                'fecha':fecha_hora,
                'valor':fila.get('valor'),
                'maximo':fila.get('maximo'),
                'minimo':fila.get('minimo'),
            }
            datos.append(dato)
    else:
        datos={
            'mensaje':'no hay datos'
        }
    return datos
