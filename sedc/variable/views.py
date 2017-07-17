# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Variable, Unidad, Control
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

#Variable views
class VariableCreate(CreateView):
    model=Variable
    fields = ['var_codigo','var_nombre','uni_id','var_maximo','var_minimo','var_sos','var_err','var_min']
    def form_valid(self, form):
        return super(VariableCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VariableCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class VariableList(ListView):
    model=Variable
    paginate_by = 100
    def get_context_data(self, **kwargs):
        context = super(VariableList, self).get_context_data(**kwargs)
    	lista=Variable.objects.all()
        page=self.request.GET.get('page')
    	paginator = Paginator(lista, 100)
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
            last=page
        context['first'] = 1
        context['last'] = paginator.num_pages
        context['range'] = range(start,last+1)
        return context

class VariableDetail(DetailView):
    model=Variable

class VariableUpdate(UpdateView):
    model=Variable
    fields = ['var_codigo','var_nombre','uni_id','var_maximo','var_minimo','var_sos','var_err','var_min']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VariableUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class VariableDelete(DeleteView):
    model=Variable
    success_url = reverse_lazy('variable:variable_index')

#Unidad
class UnidadCreate(CreateView):
    model=Unidad
    fields = ['uni_nombre','uni_sigla']
    def form_valid(self, form):
        return super(UnidadCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UnidadCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class UnidadList(ListView):
    model=Unidad
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(UnidadList, self).get_context_data(**kwargs)
    	lista=Unidad.objects.all()
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
            last=page
        context['first'] = 1
        context['last'] = paginator.num_pages
        context['range'] = range(start,last+1)
        return context

class UnidadDetail(DetailView):
    model=Unidad

class UnidadUpdate(UpdateView):
    model=Unidad
    fields = ['uni_nombre','uni_sigla']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UnidadUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class UnidadDelete(DeleteView):
    model=Unidad
    success_url = reverse_lazy('variable:unidad_index')

#Control
class ControlCreate(CreateView):
    model=Control
    fields = ['var_id','sen_id','est_id','con_fecha_ini','con_fecha_fin','con_estado']
    def form_valid(self, form):
        return super(ControlCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ControlCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class ControlList(ListView):
    model=Control
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(ControlList, self).get_context_data(**kwargs)
    	lista=Control.objects.all()
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

class ControlDetail(DetailView):
    model=Control

class ControlUpdate(UpdateView):
    model=Control
    fields = ['var_id','sen_id','est_id','con_fecha_ini','con_fecha_fin','con_estado']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ControlUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class ControlDelete(DeleteView):
    model=Control
    success_url = reverse_lazy('variable:control_index')
