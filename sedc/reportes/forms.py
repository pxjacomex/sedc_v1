# -*- coding: utf-8 -*-

from django import forms
from estacion.models import Estacion
from medicion.models import Medicion
from variable.models import Variable,Unidad
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count

import plotly.offline as opy
import plotly.graph_objs as go

class Resumen(object):
    def __init__(self, mes, maximo, minimo, medio):
        self.mes = mes
        self.maximo= maximo
        self.minimo = minimo
        self.medio = medio

class AnuarioForm(forms.Form):
    def lista_estaciones():
        lista = ()
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_nombre),)
            lista = lista + fila
        return lista

    ESTACION = lista_estaciones()
    YEAR = (
        ('2007','2007'),
        ('2008','2008'),
        ('2009','2009'),
        ('2010','2010'),
        ('2011','2011'),
        ('2012','2012'),
    )

    lista=[]
    estacion = forms.ChoiceField(required=False,choices=ESTACION,label='Estación')
    anio = forms.ChoiceField(required=False,choices=YEAR,label='Año')

    def filtrar(self,form):
        context = {}
<<<<<<< HEAD
        variables = list(Medicion.objects
            .filter(est_id=form.cleaned_data['estacion'])
            .filter(med_fecha__year=form.cleaned_data['anio'])
            .values('var_id_id').distinct('var_id_id'))
        #var_simple = [d.get('var_id_id') for d in variables]
=======

        typeI = [6,8,9,10,11]
        typeII = [1]
        typeIII = [2]
        typeIV = [3]
        typeV = [4,5]
        typeVI = [7]

        variables = list(Medicion.objects.filter(est_id=form.cleaned_data['estacion']).filter(med_fecha__year=form.cleaned_data['anio']).values('var_id_id').distinct('var_id_id'))
>>>>>>> 8efa92355d73d31f48ed5016debdcf62b1f41008
        for item in variables:
<<<<<<< HEAD
            if item.get('var_id_id') in typeI:
                matriz = self.matriz_typeI(form.cleaned_data['estacion'],str(item.get('var_id_id')),form.cleaned_data['anio'])
                grafico = self.grafico_typeI(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                context.update({str(item.get('var_id_id')) + '_grafico': grafico})
            elif item.get('var_id_id') in typeII:
                matriz = self.matriz_typeII(form.cleaned_data['estacion'],str(item.get('var_id_id')),form.cleaned_data['anio'])
                grafico = self.grafico_typeII(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                context.update({str(item.get('var_id_id')) + '_grafico': grafico})
            elif item.get('var_id_id') in typeIII:
                matriz = self.matriz_typeIII(form.cleaned_data['estacion'],str(item.get('var_id_id')),form.cleaned_data['anio'])
                grafico = self.grafico_typeIII(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                context.update({str(item.get('var_id_id')) + '_grafico': grafico})
            elif item.get('var_id_id') in typeIV:
                matriz = self.matriz_typeIV(form.cleaned_data['estacion'],str(item.get('var_id_id')),form.cleaned_data['anio'])
                grafico = self.grafico_typeIV(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                context.update({str(item.get('var_id_id')) + '_grafico': grafico})
            elif item.get('var_id_id') in typeV:
                matriz = self.matriz_typeV(form.cleaned_data['estacion'],str(item.get('var_id_id')),form.cleaned_data['anio'])
                grafico = self.grafico_typeV(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                context.update({str(item.get('var_id_id')) + '_grafico': grafico})
            elif item.get('var_id_id') in typeVI:
                matriz = self.matriz_typeVI(form.cleaned_data['estacion'],str(item.get('var_id_id')),form.cleaned_data['anio'])
                grafico = self.grafico_typeVI(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                context.update({str(item.get('var_id_id')) + '_grafico': grafico})
=======
            matriz = self.matriz_hidrologica(form.cleaned_data['estacion'],str(item.get('var_id_id')),form.cleaned_data['anio'])
            grafico = self.grafico_hidrologica(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
            context.update({str(item.get('var_id_id')) + '_matriz': matriz})
            context.update({str(item.get('var_id_id')) + '_grafico': grafico})
            context.update({'variables':self.unidad(item.get('var_id_id'))})
>>>>>>> f8cabd8e829ed5044203be1cb00dc7389193ba8a
        return context

    #consulta de maximo, minimo y promedio mensual
    def consulta_typeI(self,estacion,variable,anio):
        #annotate agrupa los valores en base a un campo y a una operacion
        consulta=Medicion.objects.filter(est_id=estacion).filter(var_id=variable).filter(med_fecha__year=anio).annotate(month=TruncMonth('med_fecha')).values('month')
        med_max=list(consulta.annotate(c=Max('med_valor')).values('c').order_by('month'))
        med_min=list(consulta.annotate(c=Min('med_valor')).values('c').order_by('month'))
        med_avg=list(consulta.annotate(c=Avg('med_valor')).values('c').order_by('month'))
        max_simple = [d.get('c') for d in med_max]
        min_simple = [d.get('c') for d in med_min]
        avg_simple = [d.get('c') for d in med_avg]
        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return max_simple,min_simple,avg_simple,meses
    def matriz_typeI(self,estacion, variable, anio):
        max_simple,min_simple,avg_simple,meses=self.consulta_typeI(estacion, variable, anio)
        matrix = []
        for i in range(len(max_simple)):
            matrix.append(Resumen(meses[i],max_simple[i],min_simple[i],avg_simple[i]))
        return matrix
    def grafico_typeI(self,estacion, variable, anio):
        max_simple,min_simple,avg_simple,meses=self.consulta_typeI(estacion, variable, anio)
        # Create and style traces
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

        # Edit the layout
        layout = go.Layout(title = str(self.titulo_grafico(variable)), yaxis={'title':'Caudal (m3/s)'})
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
        return div
    def titulo_grafico(self,variable):
        consulta=list(Variable.objects.filter(var_id=variable))
        #return consulta[0].get('var_nombre')
        return consulta[0]
    def unidad(self,variable):
        var=list(Variable.objects.filter(var_id=variable).values())
        uni=list(Unidad.objects.filter(uni_id=var[0].get('uni_id_id')))
        return uni[0]
