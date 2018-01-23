# -*- coding: utf-8 -*-

from reportes.typeI import TypeI
from reportes.typeII import TypeII
from reportes.typeIII import TypeIII
from reportes.typeIV import TypeIV
from reportes.typeV import TypeV
from reportes.typeVI import TypeVI
from cruce.models import Cruce
from estacion.models import Estacion
from medicion.models import Medicion
import datetime
import plotly.offline as opy
import plotly.graph_objs as go

from django.db import connection

def filtrar(form):
    context = {}
    #humedadsuelo,presionatmosferica,temperaturaagua,caudal,nivelagua
    typeI = [6,8,9,10,11]
    #precipitacion
    typeII = [1]
    #temperaturaaire
    typeIII = [2]
    #humedadaire
    typeIV = [3]
    #direccion y velocidad
    typeV = [4,5]
    #radiacion
    typeVI = [7]
    variables = list(Cruce.objects
        .filter(est_id=form.cleaned_data['estacion'])
        .values('var_id')
        )
    obj_typeI=TypeI()
    obj_typeII=TypeII()
    obj_typeIII=TypeIII()
    obj_typeIV=TypeIV()
    obj_typeV=TypeV()
    obj_typeVI=TypeVI()

    for item in variables:
        if item.get('var_id') in typeI:
            matriz = obj_typeI.matriz(form.cleaned_data['estacion'],item.get('var_id'),form.cleaned_data['anio'])
            grafico = obj_typeI.grafico(form.cleaned_data['estacion'],item.get('var_id'),form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
            context.update({str(item.get('var_id')) + '_grafico': grafico})
        elif item.get('var_id') in typeII:
            matriz = obj_typeII.matriz(form.cleaned_data['estacion'],item.get('var_id'),form.cleaned_data['anio'])
            grafico = obj_typeII.grafico(form.cleaned_data['estacion'],item.get('var_id'),form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
            context.update({str(item.get('var_id')) + '_grafico': grafico})
        elif item.get('var_id') in typeIII:
            matriz = obj_typeIII.matriz(form.cleaned_data['estacion'],item.get('var_id'),form.cleaned_data['anio'])
            grafico = obj_typeIII.grafico(form.cleaned_data['estacion'],item.get('var_id'),form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
            context.update({str(item.get('var_id')) + '_grafico': grafico})
        elif item.get('var_id') in typeIV:
            matriz = obj_typeIV.matriz(form.cleaned_data['estacion'],item.get('var_id'),form.cleaned_data['anio'])
            grafico = obj_typeIV.grafico(form.cleaned_data['estacion'],item.get('var_id'),form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
            context.update({str(item.get('var_id')) + '_grafico': grafico})
        elif item.get('var_id') in typeV:
            matriz = obj_typeV.matriz(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
        elif item.get('var_id') in typeVI:
            matriz = obj_typeVI.matriz(form.cleaned_data['estacion'],str(item.get('var_id')),form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
    return context
def comparar(form):
    estacion01=form.cleaned_data['estacion01']
    estacion02=form.cleaned_data['estacion02']
    estacion03=form.cleaned_data['estacion03']
    variable=form.cleaned_data['variable']
    fecha_inicio=form.cleaned_data['inicio']
    fecha_fin=form.cleaned_data['fin']
    tiempo=form.cleaned_data['tiempo']
    unidad=form.cleaned_data['unidad']
    temporalidad=conversion_tiempo(tiempo,unidad)
    val01,tiempo=datos_minutos(
        estacion01,variable,fecha_inicio,fecha_fin,'med_valor',temporalidad)
    val02,tiempo=datos_minutos(
        estacion02,variable,fecha_inicio,fecha_fin,'med_valor',temporalidad)
    val03,tiempo=datos_minutos(
        estacion03,variable,fecha_inicio,fecha_fin,'med_valor',temporalidad)
    obj_est01=Estacion.objects.get(est_id=estacion01)
    obj_est02=Estacion.objects.get(est_id=estacion02)
    obj_est03=Estacion.objects.get(est_id=estacion03)
    trace0 = go.Scatter(
        x = tiempo,
        y = val01,
        name = obj_est01.est_codigo,
        mode = 'lines',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            )
    )
    trace1 = go.Scatter(
        x = tiempo,
        y = val02,
        name = obj_est02.est_codigo,
        mode = 'lines',
        line = dict(
            color = ('rgb(50, 205, 50)'),
            )
    )
    trace2 = go.Scatter(
        x = tiempo,
        y = val03,
        name = obj_est03.est_codigo,
        mode = 'lines',
        line = dict(
            color = ('rgb(22, 96, 167)'),
            )
    )
    data = go.Data([trace0, trace1, trace2])
    layout = go.Layout(
        title = "Comparación de Estaciones",
        yaxis = dict(title='Promedios')
        )
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')
    return div


def datos_instantaneos(estacion,variable,fecha_inicio,fecha_fin,parametro):
    consulta=list(Medicion.objects.filter(est_id=estacion)
        .filter(var_id=variable).filter(med_fecha__range=[fecha_inicio,fecha_fin])
        .values(parametro,'med_fecha','med_hora')
        .order_by('med_fecha','med_hora'))
    valor=[]
    frecuencia=[]
    for fila in consulta:
        if fila.get(parametro) is not None:
            valor.append(fila.get(parametro))
        frecuencia.append(datetime.datetime.combine(fila['med_fecha'],fila['med_hora']))

    return valor,frecuencia

def datos_minutos(estacion,variable,fecha_inicio,fecha_fin,parametro,temporalidad):
    cursor = connection.cursor()
    if variable==str(1):
        cursor.execute("SELECT sum(med_valor) as valor, \
            to_timestamp(floor((extract('epoch' \
            from med_fecha+med_hora) / %s )) * %s)\
            AT TIME ZONE 'UTC' as interval_alias\
            FROM medicion_medicion\
            where est_id_id=%s and var_id_id=%s and \
            med_fecha>=%s and med_fecha<=%s\
            GROUP BY interval_alias\
            order by interval_alias",[temporalidad,temporalidad,
            estacion,variable,fecha_inicio,fecha_fin])
    else:
        cursor.execute("SELECT avg(med_valor) as valor, \
            to_timestamp(floor((extract('epoch' \
            from med_fecha+med_hora) / %s )) * %s)\
            AT TIME ZONE 'UTC' as interval_alias\
            FROM medicion_medicion\
            where est_id_id=%s and var_id_id=%s and \
            med_fecha>=%s and med_fecha<=%s\
            GROUP BY interval_alias\
            order by interval_alias",[temporalidad,temporalidad,
            estacion,variable,fecha_inicio,fecha_fin])
    datos=dictfetchall(cursor)
    valor=[]
    frecuencia=[]
    for fila in datos:
        if fila.get('valor') is not None:
            valor.append(fila.get('valor'))
        frecuencia.append(fila.get('interval_alias'))
    cursor.close()
    return valor,frecuencia
def conversion_tiempo(tiempo,unidad):
    valor=300
    print type(unidad)
    if unidad=="0":
        valor=tiempo*60
    elif unidad=="1":
        valor=tiempo*60*60
    elif unidad=="2":
        valor=tiempo*60*60*24
    elif unidad=="3":
        valor=tiempo*60*60*24*365
    return valor
def dictfetchall(cursor):
    #Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
