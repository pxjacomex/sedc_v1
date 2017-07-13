from django.views.generic.base import TemplateView
from .models import Medicion
from django.db.models import Max, Min, Avg
from django.db.models.functions import TruncMonth

import plotly.plotly as opy
import plotly.graph_objs as go

class ReportesPageView(TemplateView):
    template_name = "reportes.html"

    def get_context_data(self, **kwargs):
        context = super(ReportesPageView, self).get_context_data(**kwargs)
        #caudal 2012
        med_max=list(Medicion.objects.filter(var_id='10').annotate(month=TruncMonth('med_fecha')).values('month').annotate(c=Max('med_valor')).values('c').order_by('month'))
        med_min=list(Medicion.objects.filter(var_id='10').annotate(month=TruncMonth('med_fecha')).values('month').annotate(c=Min('med_valor')).values('c').order_by('month'))
        med_avg=list(Medicion.objects.filter(var_id='10').annotate(month=TruncMonth('med_fecha')).values('month').annotate(c=Avg('med_valor')).values('c').order_by('month'))

        max_simple = [d.get('c') for d in med_max]
        min_simple = [d.get('c') for d in med_min]
        avg_simple = [d.get('c') for d in med_avg]
        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

        matrix = []
        for i in range(len(meses)):
            matrix.append(Resumen(meses[i],max_simple[i],min_simple[i],avg_simple[i]))

        context['matrix'] = matrix
        div = PlotGrafico(meses,max_simple,min_simple,avg_simple)
        context['graph'] = div
        return context

class Resumen(object):
    def __init__(self, mes, maximo, minimo, medio):
        self.mes = mes
        self.maximo= maximo
        self.minimo = minimo
        self.medio = medio


### graficos
def PlotGrafico(meses,max_simple,min_simple,avg_simple):
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
    layout = go.Layout(title = 'Caudal Medio Mensual', xaxis={'title':'Meses'}, yaxis={'title':'Caudal (m3/s)'})
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div
