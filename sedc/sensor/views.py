# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from sensor.models import Sensor
from django.views.generic import ListView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from sensor.forms import SensorSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class SensorCreate(LoginRequiredMixin,CreateView):
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
class SensorList(LoginRequiredMixin,ListView,FormView):
    #parámetros ListView
    model=Sensor
    paginate_by=10
    #parámetros FormView
    template_name='sensor/sensor_list.html'
    form_class=SensorSearchForm
    def post(self, request, *args, **kwargs):
        form=SensorSearchForm(self.request.POST or None)
        page=kwargs.get('page')
        if form.is_valid() and self.request.is_ajax():
            self.object_list=form.filtrar(form)
        else:
            self.object_list=Sensor.objects.all()
        context = super(SensorList, self).get_context_data(**kwargs)
        context.update(pagination(self.object_list,page,10))
        return render(request,'sensor/sensor_table.html',context)
    def get_context_data(self, **kwargs):
        context = super(SensorList, self).get_context_data(**kwargs)
        page=self.request.GET.get('page')
        context.update(pagination(self.object_list,page,10))
        return context
class SensorDetail(LoginRequiredMixin,DetailView):
    model=Sensor
class SensorUpdate(LoginRequiredMixin,UpdateView):
    model=Sensor
    fields = ['sen_nombre','mar_id','sen_modelo','sen_serial']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SensorUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context
class SensorDelete(LoginRequiredMixin,DeleteView):
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
    return context
