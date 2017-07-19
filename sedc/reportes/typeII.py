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

class TypeII(Titulos):
    '''consulta y crea la matriz de datos y el grafico para variables: 1'''
    def consulta(self,estacion,variable,periodo):
        #annotate agrupa los valores en base a un campo y a una operacion
        consulta=Medicion.objects.filter(est_id=estacion).filter(var_id=variable).filter(med_fecha__year=periodo).annotate(month=TruncMonth('med_fecha')).values('month')
        med_mensual=list(consulta.annotate(c=Sum('med_valor')).values('c').order_by('month'))
        #med_max=list(consulta.annotate(c=Max('med_valor')).values('c','med_fecha').order_by('month'))
        #med_totdias=list(consulta.aggregate(c=Sum(Case(When('med_valor'>0, then=1),output_field=IntegerField()))).values('c').order_by('month'))
        #med_totdias=range(1,13)
        mensual_simple = [d.get('c') for d in med_mensual]
        #max24H_simple = [d.get('c') for d in med_max]
        #maxdia_simple = [d.get('med_fecha') for d in med_max]
        #totdias_simple = [d.get('c') for d in med_totdias]
        #totdias_simple=range(1,13)
        max24H_simple,maxdia_simple,totdias_simple = self.maximospre(estacion, variable, periodo)
        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return mensual_simple,max24H_simple,maxdia_simple,totdias_simple,meses
    def matriz(self,estacion, variable, periodo):
        mensual_simple,max24H_simple,maxdia_simple,totdias_simple,meses=self.consulta(estacion, variable, periodo)
        matrix = []
        for i in range(len(mensual_simple)):
            #matrix.append(ResTypeII(meses[i],mensual_simple[i],max24H_simple[i],maxdia_simple[i],totdias_simple[i]))
            matrix.append(ResTypeII(meses[i],mensual_simple[i],max24H_simple[i],maxdia_simple[i],totdias_simple[i]))
        return matrix
    def grafico(self,estacion, variable, periodo):
        mensual_simple,max24H_simple,maxdia_simple,totdias_simple,meses=self.consulta(estacion, variable, periodo)
        trace1 = go.Bar(
            x=meses,
            y=mensual_simple,
            name='Precipitacion (mm)'
        )
        ''' Incluir si tiene media historica
        trace2 = go.Bar(
            x=meses,
            y=media historica,
            name='Media Historica'
        )

        data = [trace1, trace2]

        layout = go.Layout(
            barmode='group'
        )
        '''
        data = go.Data([trace1])
        layout = go.Layout(title = str(self.titulo_grafico(variable)) + str(" (") + str(self.titulo_unidad(variable)) + str(")"))
        matriz = go.matriz(data=data, layout=layout)
        div = opy.plot(matriz, auto_open=False, output_type='div')
        return div

    def maximospre(self, estacion, variable, periodo):
        consulta=(Medicion.objects
        .filter(est_id=estacion)
        .filter(var_id=variable)
        .filter(med_fecha__year=periodo))
        max24H_simple = []
        maxdia_simple = []
        totdias_simple = []
        for i in range(1,13):
            consulta=consulta.filter(med_fecha__month=i)
            consulta=consulta.annotate(month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha')).values('month','day')
            consulta=consulta.annotate(valor=Sum('med_valor')).values('valor','month','day').order_by('valor')
            item = consulta[1]
            max24H_simple.append(1)
            maxdia_simple.append(1)
            count = 0
            for j in consulta:
                if j.get['valor'] > 0:
                    count+=1
            totdias_simple.append(count)
        return max24H_simple,maxdia_simple,totdias_simple
