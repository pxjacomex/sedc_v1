# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Medicion
from django.views.generic import ListView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from medicion.forms import MedicionSearchForm

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

"""class MedicionList(ListView):
    model=Medicion
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(MedicionList, self).get_context_data(**kwargs)
    	lista=Medicion.objects.all()
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
        return context"""
class MedicionList(FormView):
    template_name='medicion/medicion_list.html'
    form_class=MedicionSearchForm
    success_url='/medicion/'
    lista=[]
    def post(self, request, *args, **kwargs):
        form=MedicionSearchForm(self.request.POST or None)
        if form.is_valid():
            self.lista=form.filtrar(form)
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(MedicionList, self).get_context_data(**kwargs)
        context['lista']=self.lista
        return context

class MedicionDetail(DetailView):
    model=Medicion

class MedicionUpdate(UpdateView):
    model=Medicion
    fields = ['var_id','est_id','med_fecha','med_hora','med_valor','med_maximo',
              'med_minimo','med_validado']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class MedicionDelete(DeleteView):
    model=Medicion
    success_url = reverse_lazy('medicion:medicion_index')

#Validacion
'''
class ValidacionCreate(CreateView):
    model=Validacion
    fields = ['med_id','val_fecha','val_hora','val_valor','val_maximo','val_minimo','val_mensaje']
    def form_valid(self, form):
        return super(ValidacionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ValidacionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class ValidacionList(ListView):
    model=Validacion
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(ValidacionList, self).get_context_data(**kwargs)
    	lista=Validacion.objects.all()
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

class ValidacionDetail(DetailView):
    model=Validacion

class ValidacionUpdate(UpdateView):
    model=Validacion
    fields = ['med_id','val_fecha','val_hora','val_valor','val_maximo','val_minimo','val_mensaje']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ValidacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class ValidacionDelete(DeleteView):
    model=Validacion
    success_url = reverse_lazy('medicion:validacion_index')
'''
