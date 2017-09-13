# -*- coding: utf-8 -*-

from django import forms
from medicion.models import Medicion
from variable.models import Variable,Unidad
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
import plotly.offline as opy
import plotly.graph_objs as go
from reportes.titulos import Titulos
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)

class Resumen(object):
    def __init__(self, mes, maximo_abs, maxdia, minimo_abs, mindia, maximo, minimo, medio):
        self.mes = mes
        self.maximo_abs = maximo_abs
        self.maxdia = maxdia
        self.minimo_abs = minimo_abs
        self.mindia = mindia
        self.maximo= maximo
        self.minimo = minimo
        self.medio = medio
#clase para anuario de la variable TAI
class TypeIII(Titulos):
    '''consulta y crea la matriz de datos y el grafico para variable: 2'''
    def consulta(self,estacion,variable,periodo):
        #annotate agrupa los valores en base a un campo y a una operacion
        med_avg=list(Medicion.objects.filter(est_id=estacion)
        .filter(var_id=variable).filter(med_fecha__year=periodo)
        .annotate(month=TruncMonth('med_fecha')).values('month')
        .annotate(c=Avg('med_valor')).values('c').order_by('month'))

        consulta_max=(Medicion.objects.filter(est_id=estacion)
            .filter(var_id=variable).filter(med_fecha__year=periodo)
            .exclude(med_maximo=None))
        if consulta_max.count()>0:
            datos_diarios_max=list(consulta_max.annotate(
            month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha'))
            .values('month','day').annotate(valor=Max('med_maximo'))
            .values('valor','month','day').order_by('month','day'))
        else:
            datos_diarios_max=list(Medicion.objects.filter(est_id=estacion)
                .filter(var_id=variable).filter(med_fecha__year=periodo)
                .annotate(month=ExtractMonth('med_fecha'),
                    day=ExtractDay('med_fecha'))
                .values('month','day').annotate(valor=Max('med_valor'))
                .values('valor','month','day').order_by('month','day'))
        max_abs_simple,maxdia_simple,max_simple = self.maximostai(datos_diarios_max)
        consulta_min=(Medicion.objects.filter(est_id=estacion)
            .filter(var_id=variable).filter(med_fecha__year=periodo)
            .exclude(med_minimo=None))
        if consulta_min.count()>0:
            datos_diarios_min=list(consulta_min.annotate(
            month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha'))
            .values('month','day').annotate(valor=Min('med_minimo'))
            .values('valor','month','day').order_by('month','day'))
        else:
            datos_diarios_min=list(Medicion.objects.filter(est_id=estacion)
                .filter(var_id=variable).filter(med_fecha__year=periodo)
                .exclude(med_valor=None)
                .annotate(month=ExtractMonth('med_fecha'),
                    day=ExtractDay('med_fecha'))
                .values('month','day').annotate(valor=Min('med_valor'))
                .values('valor','month','day').order_by('month','day'))

        min_abs_simple,mindia_simple,min_simple = self.minimostai(datos_diarios_min)
        avg_simple = [d.get('c') for d in med_avg]
        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return max_abs_simple,maxdia_simple,min_abs_simple,mindia_simple,max_simple,min_simple,avg_simple,meses
    def matriz(self,estacion, variable, periodo):
        max_abs_simple,maxdia_simple,min_abs_simple,mindia_simple,max_simple,min_simple,avg_simple,meses=self.consulta(estacion, variable, periodo)
        matrix = []
        for i in range(len(meses)):
            matrix.append(Resumen(meses[i],max_abs_simple[i],maxdia_simple[i],min_abs_simple[i],mindia_simple[i],max_simple[i],min_simple[i],avg_simple[i]))
        return matrix
    def grafico(self,estacion, variable, periodo):
        max_abs_simple,maxdia_simple,min_abs_simple,mindia_simple,max_simple,min_simple,avg_simple,meses=self.consulta(estacion, variable, periodo)
        trace0 = go.Scatter(
            x = meses,
            y = max_simple,
            name = 'Max',
            line = dict(
                color = ('rgb(22, 96, 167)'),
                width = 4)
        )
        trace1 = go.Scatter(
            x = meses,
            y = min_simple,
            name = 'Min',
            line = dict(
                color = ('rgb(205, 12, 24)'),
                width = 4,)
        )
        trace2 = go.Scatter(
            x = meses,
            y = avg_simple,
            name = 'Media',
            line = dict(
                color = ('rgb(50, 205, 50)'),
                width = 4,)
        )
        data = go.Data([trace0, trace1, trace2])
        layout = go.Layout(title = str(self.titulo_grafico(variable)) + str(" (") + str(self.titulo_unidad(variable)) + str(")"))
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
        return div

    def maximostai(self, datos_diarios_max):
        # retorna maxima temp mensual y en que dia sucedio y media mensual de las maximas

        max_abs = []
        maxdia = []
        avgmax = []
        for i in range(1,13):
            val_max_abs=[]
            val_maxdia = []
            for fila in datos_diarios_max:
                if fila.get('month') == i:
                    val_max_abs.append(fila.get('valor'))
                    val_maxdia.append(fila.get('day'))
            max_abs.append(max(val_max_abs))
            maxdia.append(val_maxdia[val_max_abs.index(max(val_max_abs))])
            #avgmax.append(sum(val_max_abs) / (len(val_max_abs)))
            avgmax.append((len(val_max_abs)))
        return max_abs,maxdia, avgmax

    def minimostai(self, datos_diarios_min):
        # retorna minima temp mensual y en que dia sucedio y media mensual de las minimas

        min_abs = []
        mindia = []
        avgmin = []
        for i in range(1,13):
            val_min_abs=[]
            val_mindia = []
            for fila in datos_diarios_min:
                if fila.get('month') == i:
                    val_min_abs.append(fila.get('valor'))
                    val_mindia.append(fila.get('day'))
            min_abs.append(min(val_min_abs))
            mindia.append(val_mindia[val_min_abs.index(min(val_min_abs))])
            #avgmin.append(sum(val_min_abs) / (len(val_min_abs)))
            avgmin.append((len(val_min_abs)))
        return min_abs,mindia,avgmin
