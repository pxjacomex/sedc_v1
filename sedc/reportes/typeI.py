# -*- coding: utf-8 -*-

from django import forms
from medicion.models import Medicion
from variable.models import Variable,Unidad
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
import plotly.offline as opy
import plotly.graph_objs as go
from reportes.titulos import Titulos

class Resumen(object):
    def __init__(self, mes, maximo, minimo, medio):
        self.mes = mes
        self.maximo= maximo
        self.minimo = minimo
        self.medio = medio
#clase para anuario de las las variables HSU, PAT, TAG, CAU, NAG
class TypeI(Titulos):
    '''consulta y crea la matriz de datos y el grafico para variables: 6,8,9,10,11'''
    def consulta(self,estacion,variable,periodo):
        #annotate agrupa los valores en base a un campo y a una operacion
        consulta=Medicion.objects.filter(est_id=estacion).filter(var_id=variable).filter(med_fecha__year=periodo)
        if variable == 8:
            consulta = consulta.exclude(med_valor = 0, med_maximo = 0, med_minimo = 0)
        consulta=consulta.annotate(month=TruncMonth('med_fecha')).values('month')
        med_max=list(consulta.annotate(c=Max('med_valor')).values('c').order_by('month'))
        med_min=list(consulta.annotate(c=Min('med_valor')).values('c').order_by('month'))
        med_avg=list(consulta.annotate(c=Avg('med_valor')).values('c').order_by('month'))
        max_simple = [d.get('c') for d in med_max]
        min_simple = [d.get('c') for d in med_min]
        avg_simple = [d.get('c') for d in med_avg]
        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return max_simple,min_simple,avg_simple,meses
    def matriz(self,estacion, variable, periodo):
        max_simple,min_simple,avg_simple,meses=self.consulta(estacion, variable, periodo)
        matrix = []
        for i in range(len(max_simple)):
            matrix.append(Resumen(meses[i],max_simple[i],min_simple[i],avg_simple[i]))
        return matrix
    def grafico(self,estacion, variable, periodo):
        max_simple,min_simple,avg_simple,meses=self.consulta(estacion, variable, periodo)
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
