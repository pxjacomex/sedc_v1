# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Datalogger, Sensor
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

#Datalogger views
class DataloggerCreate(CreateView):
    model = Datalogger
    fields = ['dat_codigo','dat_nombre','dat_marca','dat_modelo','dat_serial']
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
    	paginator = Paginator(lista, 2)
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
    fields = ['dat_codigo','dat_nombre','dat_marca','dat_modelo','dat_serial']
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
    fields = ['dat_id','sen_codigo','sen_nombre','sen_marca','sen_modelo','sen_serial']
    def form_valid(self, form):
        return super(SensorCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SensorCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class SensorList(ListView):
    model=Sensor
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(SensorList, self).get_context_data(**kwargs)
    	lista=Sensor.objects.all()
        page=self.request.GET.get('page')
    	paginator = Paginator(lista, 2)
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

class SensorDetail(DetailView):
    model=Sensor

class SensorUpdate(UpdateView):
    model=Sensor
    fields = ['dat_id','sen_codigo','sen_nombre','sen_marca','sen_modelo','sen_serial']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SensorUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class SensorDelete(DeleteView):
    model=Sensor
    success_url = reverse_lazy('datalogger:sensor_index')
