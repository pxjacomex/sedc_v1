# -*- coding: utf-8 -*-

from django import forms
from medicion.models import Medicion
from variable.models import Variable,Unidad
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Max, Case, When, IntegerField
import plotly.offline as opy
import plotly.graph_objs as go
from reportes.titulos import Titulos
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)

class ResTypeII(object):
    def __init__(self, mes, mensual, max24H, maxdia, totdias):
        self.mes = mes
        self.mensual = mensual
        self.max24H = max24H
        self.maxdia = maxdia
        self.totdias = totdias
#clase para la variable PRE
class TypeII(Titulos):
    '''consulta y crea la matriz de datos y el grafico para variables: 1'''
    def consulta(self,estacion,variable,periodo):
        #annotate agrupa los valores en base a un campo y a una operacion
        consulta=(Medicion.objects.filter(est_id=estacion)
            .filter(var_id=variable).filter(med_fecha__year=periodo)
            .annotate(month=TruncMonth('med_fecha')).values('month'))
        med_mensual=list(consulta.annotate(c=Sum('med_valor')).
            values('c').order_by('month'))
        datos_diarios=list(Medicion.objects
            .filter(est_id=estacion)
            .filter(var_id=variable)
            .filter(med_fecha__year=periodo)
            .annotate(month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha'))
            .values('month','day')
            .annotate(valor=Sum('med_valor'))
            .values('valor','month','day').order_by('month','day'))

        mensual_simple = [d.get('c') for d in med_mensual]
        max24H_simple,maxdia_simple,totdias_simple = self.maximospre(datos_diarios)
        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return mensual_simple,max24H_simple,maxdia_simple,totdias_simple,meses
    def matriz(self,estacion, variable, periodo):
        mensual_simple,max24H_simple,maxdia_simple,totdias_simple,meses=self.consulta(estacion, variable, periodo)
        matrix = []
        for i in range(len(mensual_simple)):
            matrix.append(ResTypeII(meses[i],mensual_simple[i],max24H_simple[i],maxdia_simple[i],totdias_simple[i]))
        return matrix
    def grafico(self,estacion, variable, periodo):
        mensual_simple,max24H_simple,maxdia_simple,totdias_simple,meses=self.consulta(estacion, variable, periodo)
        '''
        data=[go.Bar(
            x=meses,
            y=mensual_simple
        )]

        div = opy.plot(data, auto_open=False, output_type='div')
        return div
        '''
        trace1 = go.Bar(
            x=meses,
            y=mensual_simple,
            name='Precipitacion (mm)'
        )

        data = go.Data([trace1])
        layout = go.Layout(title = str(self.titulo_grafico(variable)) + str(" (") + str(self.titulo_unidad(variable)) + str(")"))
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
        return div


    def maximospre(self, datos_diarios):
        max24H = []
        maxdia = []
        totdias= []
        for i in range(1,13):
            val_max24h=[]
            val_maxdia = []
            val_totdias= []
            for fila in datos_diarios:
                if fila.get('month') == i:
                    val_max24h.append(fila.get('valor'))
                    val_maxdia.append(fila.get('day'))
            count = 0
            for j in val_max24h:
                if(j>0):
                    count+=1
            max24H.append(max(val_max24h))
            maxdia.append(val_maxdia[val_max24h.index(max(val_max24h))])
            totdias.append(count)
        return max24H,maxdia,totdias
