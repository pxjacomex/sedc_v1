from django.views.generic.base import TemplateView
from django.views.generic import FormView
from reportes.forms import AnuarioForm
from reportes.consultas.forms import MedicionSearchForm

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
    valores=[]
    grafico =[]
    #def get(self, request, *args, **kwargs):

    def post(self, request, *args, **kwargs):
        form=MedicionSearchForm(self.request.POST or None)
        if form.is_valid():
            self.lista=form.filtrar(form)
            self.frecuencia=form.cleaned_data["frecuencia"]
            self.grafico=form.grafico(form)
            if 'visualizar'in request.POST:
                return self.export_datos(self.lista,self.frecuencia)
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(ConsultasPeriodo, self).get_context_data(**kwargs)
        context['lista']=self.lista
        context['frecuencia']=self.frecuencia
        context['valores']=self.valores
        context['grafico']=self.grafico
        return context
    def export_datos(self,datos,frecuencia):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        writer = csv.writer(response)
        if frecuencia=="1":
            writer.writerow(['anio', 'mes','dia','hora','valor'])
            for fila in datos:
                writer.writerow([fila.get('year'), fila.get('month')
                    , fila.get('day'), fila.get('hour'), fila.get('valor')])
        elif frecuencia=="2":
            writer.writerow(['anio', 'mes','dia','valor'])
            for fila in datos:
                writer.writerow([fila.get('year'), fila.get('month')
                    , fila.get('day'), fila.get('valor')])

        else:
            writer.writerow(['anio','mes', 'valor'])
            for fila in datos:
                writer.writerow([fila.get('year'), fila.get('month'),
                fila.get('valor')])
        return response
