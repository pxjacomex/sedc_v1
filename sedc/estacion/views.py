# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Estacion
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

# Create your views here.
class EstacionCreate(CreateView):
    model = Estacion
    fields = ['est_id', 'est_codigo','est_nombre','est_tipo','est_provincia','est_latitud','est_longitud','est_altura','est_ficha']
    def form_valid(self, form):
        return super(EstacionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EstacionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

# Create your views here.
class EstacionList(ListView):
    model=Estacion
    paginate_by = 2
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EstacionList, self).get_context_data(**kwargs)
    	lista=Estacion.objects.all()
        page=self.request.GET.get('page')
    	paginator = Paginator(lista, 2)
    	if page is None:
    	    page=1
    	else:
    	    page=int(self.request.GET.get('page'))

    	if page == 1:
    	    start=1
            last=start+2
    	elif page == paginator.num_pages:
            last=paginator.num_pages
            start=last-2
        else:
    	    start=page-1
            last=page+1
        context['first'] = 1
        context['last'] = paginator.num_pages
        context['range'] = range(start,last+1)
        return context

class EstacionDetail(DetailView):
    model=Estacion
class EstacionUpdate(UpdateView):
    model=Estacion
    fields = ['est_id', 'est_codigo','est_nombre','est_tipo','est_provincia','est_latitud','est_longitud','est_altura','est_ficha']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EstacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context
class EstacionDelete(DeleteView):
    model=Estacion
    success_url = reverse_lazy('estacion:estacion_index')
