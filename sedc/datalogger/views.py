# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import Datalogger, Sensor
from django.views.generic import ListView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import SensorSearchForm

#Datalogger views
class DataloggerCreate(CreateView):
    model = Datalogger
    fields = ['est_id','dat_codigo','dat_marca','dat_modelo','dat_serial']
    def form_valid(self, form):
        return super(DataloggerCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DataloggerCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class DataloggerList(ListView):
    model=Datalogger
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(DataloggerList, self).get_context_data(**kwargs)
    	lista=Datalogger.objects.all()
        page=self.request.GET.get('page')
    	paginator = Paginator(lista, 10)
    	if page is None:
    	    page=1
    	else:
    	    page=int(self.request.GET.get('page'))
    	if page == 1:
    	    start=1
            last=start+1
    	elif page == paginator.num_pages:
            last=paginator.num_pages
            start=last-1
        else:
    	    start=page-1
            last=page+1
        context['first'] = 1
        context['last'] = paginator.num_pages
        context['range'] = range(start,last+1)
        return context

class DataloggerDetail(DetailView):
    model=Datalogger

class DataloggerUpdate(UpdateView):
    model=Datalogger
    fields = ['est_id','dat_codigo','dat_marca','dat_modelo','dat_serial']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DataloggerUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class DataloggerDelete(DeleteView):
    model=Datalogger
    success_url = reverse_lazy('datalogger:datalogger_index')

#Sensor
class SensorCreate(CreateView):
    model = Sensor
    fields = ['sen_nombre','sen_marca','sen_modelo','sen_serial']
    def form_valid(self, form):
        return super(SensorCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SensorCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context
#class SensorSearch(FormView,ListView):
class SensorSearch(FormView):
    template_name='datalogger/list_search.html'
    form_class=SensorSearchForm
    success_url='/sensor/search/'
    lista=[]
    def post(self, request, *args, **kwargs):
        form=SensorSearchForm(self.request.POST or None)
        if form.is_valid():
            self.lista=form.filtrar(form)
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(SensorSearch, self).get_context_data(**kwargs)
        context['lista']=self.lista
        return context
class SensorList(ListView):
    model=Sensor
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(SensorList, self).get_context_data(**kwargs)
        page=self.request.GET.get('page')
        context.update(pagination(self.get_queryset(),page,10))
        return context
#HEAD
    def get_queryset(self):
        self.sen_nombre=self.request.GET.get('sen_nombre')
        self.sen_marca=self.request.GET.get('sen_marca')
        page= self.request.GET.get('page') if None else 1
        Lista={}
        if self.sen_nombre is None and self.sen_marca is None:
            Lista=Sensor.objects.all()
        if self.sen_nombre is '' and self.sen_marca is 'source ':
            Lista=Sensor.objects.all()
        elif self.sen_nombre == '':
            Lista=Sensor.objects.filter(sen_marca=self.sen_marca)
        elif self.sen_marca == '':
            Lista=Sensor.objects.filter(sen_nombre=self.sen_nombre)
        elif page!=0 or self.sen_nombre == '' or self.sen_marca == '':
            Lista=Sensor.objects.all()
        else:
            Lista=Sensor.objects.filter(sen_nombre=self.sen_nombre).filter(sen_marca=self.sen_marca)
        return Lista

#e0a13a3ea02aa825f98e00d6fc23bd5fa2053bcd

class SensorDetail(DetailView):
    model=Sensor

class SensorUpdate(UpdateView):
    model=Sensor
    fields = ['sen_nombre','sen_marca','sen_modelo','sen_serial']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SensorUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class SensorDelete(DeleteView):
    model=Sensor
    success_url = reverse_lazy('datalogger:sensor_index')

def pagination(lista,page,num_reg):
    #lista=model.objects.all()
    paginator = Paginator(lista, num_reg)
    if page is None:
        page=1
    else:
        page=int(page)
    if page == 1:
        start=1
        last=start+1
    elif page == paginator.num_pages:
        last=paginator.num_pages
        start=last-1
    else:
        start=page-1
        last=page+1
    context={
        'first':'1',
        'last':paginator.num_pages,
        'range':range(start,last+1),
    }
    return context
def options_sensor():
    TIPO_MARCA=(
        ('CAMPBELL'),
        ('VAISALA'),
        ('YOUNG'),
        ('APOGEE'),
        ('TEXAS ELECTRONICS'),
        ('HOBO'),
        )
    TIPO_NOMBRE=(
        ('Termómetro'),
        ('Higrómetro'),
        ('Pluviógrafo'),
        ('Veleta'),
        ('Anemómetro'),
        ('Barómetro'),
        ('TDR'),
        ('Piranómetro'),
        ('Termómetro de agua'),
        ('Sensor de nivel'),
        )
    #TIPO_NOMBRE=map(TIPO_NOMBRE.encode('utf-8'))
    #TIPO_NOMBRE = [[word.encode("utf8") for word in sets] for sets in TIPO_NOMBRE]
    context = {
        'TIPO_NOMBRE':TIPO_NOMBRE,
        'TIPO_MARCA':TIPO_MARCA,
    }
    return context
