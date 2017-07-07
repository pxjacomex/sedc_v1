# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Vacios
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

# Create your views here.
#Vacios
class VaciosCreate(CreateView):
    model=Vacios
    fields = ['est_id','var_id','vac_fecha_ini','vac_hora_ini','vac_fecha_fin','vac_hora_fin','vac_observacion']
    def form_valid(self, form):
        return super(VaciosCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VaciosCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class VaciosList(ListView):
    model=Vacios
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(VaciosList, self).get_context_data(**kwargs)
    	lista=Vacios.objects.all()
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

class VaciosDetail(DetailView):
    model=Vacios

class VaciosUpdate(UpdateView):
    model=Vacios
    fields = ['est_id','var_id','vac_fecha_ini','vac_hora_ini','vac_fecha_fin','vac_hora_fin','vac_observacion']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VaciosUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class VaciosDelete(DeleteView):
    model=Vacios
    success_url = reverse_lazy('vacios:vacios_index')
