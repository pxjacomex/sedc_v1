# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#from sensor.models import Sensor
from django.views.generic import ListView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
#from sensor.forms import SensorSearchForm

# Create your views here.
'''class SensorCreate(CreateView):
    model = Sensor
    fields = ['sen_nombre','mar_id','sen_modelo','sen_serial']
    def form_valid(self, form):
        return super(SensorCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SensorCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class SensorList(ListView,FormView):
    #parámetros ListView
    model=Sensor
    paginate_by=10
    #parámetros FormView
    template_name='sensor/sensor_list.html'
    form_class=SensorSearchForm
    #success_url='/sensor/'
    #parametros propios
    cadena=str("")
    def get(self, request, *args, **kwargs):

        form=SensorSearchForm(self.request.GET or None)
        self.object_list=Sensor.objects.all()
        if form.is_valid():
            self.object_list=form.filtrar(form)
            self.cadena=form.cadena(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(SensorList, self).get_context_data(**kwargs)
        #page=kwargs.get('page')
        #context.update(pagination(self.object_list,page,10))
        context["cadena"]=self.cadena
        return context

class SensorDetail(DetailView):
    model=Sensor

class SensorUpdate(UpdateView):
    model=Sensor
    fields = ['sen_nombre','mar_id','sen_modelo','sen_serial']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SensorUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class SensorDelete(DeleteView):
    model=Sensor
    success_url = reverse_lazy('sensor:sensor_index')

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
    return context'''
