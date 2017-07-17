from django import forms
from estacion.models import Estacion
from medicion.models import Medicion
from variable.models import Variable
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
    estacion = forms.ChoiceField(required=False,choices=ESTACION)
    anio = forms.ChoiceField(required=False,choices=YEAR)

    def filtrar(self,form):
        context = {}
        variables = list(Medicion.objects.filter(est_id=form.cleaned_data['estacion']).filter(med_fecha__year=form.cleaned_data['anio']).values('var_id_id').distinct('var_id_id'))
        var_simple = [d.get('var_id_id') for d in variables]

        for i in var_simple:
            matriz = self.matrix(form.cleaned_data['estacion'],str(i),form.cleaned_data['anio'])
            context.update({'variables':i})
            #grafico = self.PlotGrafico(form.cleaned_data['estacion'],'10',form.cleaned_data['anio'])
            context.update({str(i) + '_matriz': matriz})
            #context.update({str(var_simple[i]) + '_grapfico': grafico})

        return context

    def matrix(self,estacion, variable, anio):
        med_max=list(Medicion.objects.filter(est_id=estacion).filter(var_id=variable).filter(med_fecha__year=anio).annotate(month=TruncMonth('med_fecha')).values('month').annotate(c=Max('med_valor')).values('c').order_by('month'))
        med_min=list(Medicion.objects.filter(est_id=estacion).filter(var_id=variable).filter(med_fecha__year=anio).annotate(month=TruncMonth('med_fecha')).values('month').annotate(c=Min('med_valor')).values('c').order_by('month'))
        med_avg=list(Medicion.objects.filter(est_id=estacion).filter(var_id=variable).filter(med_fecha__year=anio).annotate(month=TruncMonth('med_fecha')).values('month').annotate(c=Avg('med_valor')).values('c').order_by('month'))

        max_simple = [d.get('c') for d in med_max]
        min_simple = [d.get('c') for d in med_min]
        avg_simple = [d.get('c') for d in med_avg]
        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

        matrix = []
        for i in range(len(meses)):
            matrix.append(Resumen(meses[i],max_simple[i],min_simple[i],avg_simple[i]))
        return matrix
    def PlotGrafico(self,estacion, variable, anio):
        med_max=list(Medicion.objects.filter(est_id=estacion).filter(var_id=variable).filter(med_fecha__year=anio).annotate(month=TruncMonth('med_fecha')).values('month').annotate(c=Max('med_valor')).values('c').order_by('month'))
        med_min=list(Medicion.objects.filter(est_id=estacion).filter(var_id=variable).filter(med_fecha__year=anio).annotate(month=TruncMonth('med_fecha')).values('month').annotate(c=Min('med_valor')).values('c').order_by('month'))
        med_avg=list(Medicion.objects.filter(est_id=estacion).filter(var_id=variable).filter(med_fecha__year=anio).annotate(month=TruncMonth('med_fecha')).values('month').annotate(c=Avg('med_valor')).values('c').order_by('month'))

        max_simple = [d.get('c') for d in med_max]
        min_simple = [d.get('c') for d in med_min]
        avg_simple = [d.get('c') for d in med_avg]
        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

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
        layout = go.Layout(title = "Caudal Medio Mensual", yaxis={'title':'Caudal (m3/s)'})
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
        return div
