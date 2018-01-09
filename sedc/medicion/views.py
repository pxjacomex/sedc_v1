# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Medicion
from django.views.generic import ListView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from medicion.forms import MedicionSearchForm,FilterDeleteForm
from medicion.functions import filtrar,datos_variable,consultar,eliminar
from django.db import connection

#Medicion views
class MedicionCreate(CreateView):
    model=Medicion
    fields = ['var_id','est_id','med_fecha','med_hora','med_valor','med_maximo',
              'med_minimo','med_validado']
    def form_valid(self, form):
        return super(MedicionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

#Lista de datos crudos
class MedicionList(FormView):
    template_name='medicion/medicion_list.html'
    form_class=MedicionSearchForm
    success_url='/medicion/'
    lista=[]
    variable=""
    def post(self, request, *args, **kwargs):
        form=MedicionSearchForm(self.request.POST or None)
        if form.is_valid():
            self.lista=filtrar(form)
            self.variable=datos_variable(form)
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(MedicionList, self).get_context_data(**kwargs)
        context['lista']=self.lista
        context['variable']=self.variable
        return context
#Clase para filtrar datos para la vista delete
class ListDelete(FormView):
    template_name='medicion/list_delete.html'
    form_class=FilterDeleteForm
    success_url='/medicion/listdelete/'
    lista=[]
    variable=""
    def post(self, request, *args, **kwargs):
        form=FilterDeleteForm(self.request.POST or None)
        if form.is_valid():
            self.lista=consultar(form)
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(ListDelete, self).get_context_data(**kwargs)
        context['lista']=self.lista
        return context
#filtro de Datos Crudos
class MedicionFilter(FormView):
    template_name='medicion/medicion_filter.html'
    form_class=MedicionSearchForm
    success_url='/medicion/filter/'


#filtro para eliminar los datos
class FilterDelete(FormView):
    template_name='medicion/filter_delete.html'
    form_class=FilterDeleteForm
    success_url='/medicion/filterdelete/'
    #mensaje de confirmación
    mensaje=""
    def post(self,request,*args,**kwargs):
        form=FilterDeleteForm(self.request.POST or None)
        if form.is_valid():
            eliminar(form)
            self.mensaje="Datos Eliminados"
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(FilterDelete, self).get_context_data(**kwargs)
        context['mensaje']=self.mensaje
        return context


class MedicionDetail(DetailView):
    model=Medicion

class MedicionUpdate(UpdateView):
    model=Medicion
    fields = ['med_valor','med_maximo','med_minimo']
    url=""
    def get(self, request, *args, **kwargs):
        #print kwargs.get('pk')
        med_id=kwargs.get('pk')
        med_fecha=kwargs.get('fecha')
        med_hora=kwargs.get('hora')
        obj_medicion=Medicion.objects.filter(med_fecha=med_fecha)\
        .filter(med_hora=med_hora).get(med_id=med_id)
        self.object=obj_medicion
        self.url="/medicion/"+med_id+"/"+med_fecha+"/"+med_hora+"/"
        return self.render_to_response(self.get_context_data(**kwargs))
    def post(self, request, *args, **kwargs):
        med_id=kwargs.get('pk')
        med_fecha=kwargs.get('fecha')
        med_hora=kwargs.get('hora')
        obj_medicion=Medicion.objects.filter(med_fecha=med_fecha)\
        .filter(med_hora=med_hora).get(med_id=med_id)
        data=request.POST
        with connection.cursor() as cursor:
            cursor.execute("UPDATE medicion_medicion SET med_valor = %s, \
            med_maximo=%s, med_minimo=%s  WHERE med_fecha = %s \
            and med_hora=%s and med_id=%s",[data.get('med_valor'),
            data.get('med_maximo'),data.get('med_minimo'),med_fecha,med_hora,
            med_id])
        self.object=obj_medicion
        return self.render_to_response(self.get_context_data(**kwargs))
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        context['url']=self.url
        return context

class MedicionDelete(UpdateView):
    model=Medicion
    fields = ['est_id','var_id','med_fecha','med_valor','med_valor','med_maximo','med_minimo']
    url=""
    template_name='medicion/medicion_delete.html'
    def get(self, request, *args, **kwargs):
        med_id=kwargs.get('pk')
        med_fecha=kwargs.get('fecha')
        med_hora=kwargs.get('hora')
        obj_medicion=Medicion.objects.filter(med_fecha=med_fecha)\
        .filter(med_hora=med_hora).get(med_id=med_id)
        self.object=obj_medicion
        self.url="/medicion/delete/"+med_id+"/"+med_fecha+"/"+med_hora+"/"
        return self.render_to_response(self.get_context_data(**kwargs))
    def post(self, request, *args, **kwargs):
        med_id=kwargs.get('pk')
        med_fecha=kwargs.get('fecha')
        med_hora=kwargs.get('hora')
        obj_medicion=Medicion.objects.filter(med_fecha=med_fecha)\
        .filter(med_hora=med_hora).get(med_id=med_id)
        data=request.POST
        with connection.cursor() as cursor:
            cursor.execute("UPDATE medicion_medicion SET med_estado = false \
            WHERE med_fecha = %s \
            and med_hora=%s and med_id=%s",[med_fecha,med_hora,med_id])
        self.object=obj_medicion
        return self.render_to_response(self.get_context_data(**kwargs))
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionDelete, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        context['url']=self.url
        return context
