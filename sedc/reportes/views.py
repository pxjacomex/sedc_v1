from django.views.generic.base import TemplateView
#from .models import Medicion
#from django.db.models import Max, Min, Avg
#from django.db.models.functions import TruncMonth
from django.views.generic import FormView
from reportes.forms import AnuarioForm
from reportes.consultas.forms import MedicionSearchForm
#import plotly.offline as opy
#import plotly.graph_objs as go
import csv
from django.http import HttpResponse
from django.template import loader, Context
class Resumen(object):
    def __init__(self, mes, maximo, minimo, medio):
        self.mes = mes
        self.maximo= maximo
        self.minimo = minimo
        self.medio = medio


class ReportesAnuario(FormView):
    template_name='reportes/anuario_reporte.html'
    form_class=AnuarioForm
    success_url='/reportes/anuario/'
    lista={}
    def post(self, request, *args, **kwargs):
        form=AnuarioForm(self.request.POST or None)
        if form.is_valid():
            self.lista=form.filtrar(form)
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(ReportesAnuario, self).get_context_data(**kwargs)
        context.update(self.lista)
        return context
#consultas por periodo y frecuencia horaria, diaria y mensual
class ConsultasPeriodo(FormView):
    template_name='reportes/consultas_periodo.html'
    form_class=MedicionSearchForm
    success_url='/reportes/consultas'
    lista=[]
    frecuencia=str("")
    consulta=str("")
    def post(self, request, *args, **kwargs):
        form=MedicionSearchForm(self.request.POST or None)
        if form.is_valid():
            self.lista=form.filtrar(form)
            self.frecuencia=form.cleaned_data["frecuencia"]
            self.consulta=form.cadena(form)


        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(ConsultasPeriodo, self).get_context_data(**kwargs)
        context['lista']=self.lista
        context['frecuencia']=self.frecuencia
        context['consulta']=self.consulta
        return context
    def export_datos(self,datos,frecuencia):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        writer.writerow(['Mes', 'Valor'])
        for fila in datos:
            writer.writerow([fila.get('time'), fila.get('valor')])

        return response
