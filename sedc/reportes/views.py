from django.views.generic.base import TemplateView
from django.views.generic import FormView
from reportes.forms import AnuarioForm
from cruce.forms import CruceSearchForm
from consultas.forms import MedicionSearchForm
import csv
from django.http import HttpResponse
from django.template import loader, Context
from consultas.functions import grafico

from django.shortcuts import render

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
    #lista=[]
    frecuencia=str("")
    valores=[]
    grafico =[]
    #def get(self, request, *args, **kwargs):

    def post(self, request, *args, **kwargs):
        form=MedicionSearchForm(self.request.POST or None)
        if form.is_valid():
            #self.lista=form.filtrar(form)
            self.frecuencia=form.cleaned_data["frecuencia"]
            if self.request.is_ajax():

                if form.exists(form):
                    self.grafico=grafico(form)
                return render(request,'reportes/consultas/grafico.html',
                    {'grafico':self.grafico,'frecuencia':self.frecuencia})
            else:
                self.lista=form.filtrar(form)
                return self.export_datos(self.lista,self.frecuencia)
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(ConsultasPeriodo, self).get_context_data(**kwargs)
        #context['lista']=self.lista
        context['frecuencia']=self.frecuencia
        context['valores']=self.valores
        context['grafico']=self.grafico
        return context
    def export_datos(self,datos,frecuencia):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte.csv"'
        writer = csv.writer(response)
        if frecuencia=="0":
            writer.writerow(['med_fecha', 'med_hora','med_valor','med_maximo','med_minimo'])
            for fila in datos:
                writer.writerow([fila.get('med_fecha'), fila.get('med_hora')
                    , fila.get('med_valor'), fila.get('med_maximo'),
                    fila.get('minimo')])
        elif frecuencia=="1":
            writer.writerow(['fecha','valor'])
            for fila in datos:
                writer.writerow([fila.get('interval_alias'), fila.get('valor'),
                    fila.get('maximo'),fila.get('minimo')])
        elif frecuencia=="2":
            writer.writerow(['anio', 'mes','dia','hora','valor','maximo','minimo'])
            for fila in datos:
                writer.writerow([fila.get('year'), fila.get('month')
                    , fila.get('day'), fila.get('hour'), fila.get('valor'),
                    fila.get('maximo'),fila.get('minimo')])
        elif frecuencia=="3":
            writer.writerow(['anio', 'mes','dia','valor','maximo','minimo'])
            for fila in datos:
                writer.writerow([fila.get('year'), fila.get('month')
                    , fila.get('day'), fila.get('valor'),
                    fila.get('maximo'),fila.get('minimo')])

        else:
            writer.writerow(['anio','mes', 'valor','maximo','minimo'])
            for fila in datos:
                writer.writerow([fila.get('year'), fila.get('month'),
                fila.get('valor'),fila.get('maximo'),fila.get('minimo')])
        return response
