# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Formato, Extension, Delimitador, Clasificacion, Asociacion
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

#Formato views
class FormatoCreate(CreateView):
    model = Formato
    fields = ['ext_id','del_id','for_nombre','for_descripcion','for_ubicacion',
              'for_archivo','for_num_col','for_fil_ini','for_fecha','for_col_fecha','for_hora',
              'for_col_hora']
    def form_valid(self, form):
        return super(FormatoCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FormatoCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class FormatoList(ListView):
    model=Formato
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(FormatoList, self).get_context_data(**kwargs)
    	lista=Formato.objects.all()
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

class FormatoDetail(DetailView):
    model=Formato

class FormatoUpdate(UpdateView):
    model=Formato
    fields = ['ext_id','del_id','for_nombre','for_descripcion','for_ubicacion',
              'for_archivo','for_num_col','for_fil_ini','for_fecha','for_col_fecha','for_hora',
              'for_col_hora']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FormatoUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class FormatoDelete(DeleteView):
    model=Formato
    success_url = reverse_lazy('formato:formato_index')

#Extension
class ExtensionCreate(CreateView):
    model=Extension
    fields = ['ext_valor']
    def form_valid(self, form):
        return super(ExtensionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ExtensionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class ExtensionList(ListView):
    model=Extension
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(ExtensionList, self).get_context_data(**kwargs)
    	lista=Extension.objects.all()
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

class ExtensionDetail(DetailView):
    model=Extension

class ExtensionUpdate(UpdateView):
    model=Extension
    fields = ['ext_valor']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ExtensionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class ExtensionDelete(DeleteView):
    model=Extension
    success_url = reverse_lazy('formato:extension_index')

#Delimitador
class DelimitadorCreate(CreateView):
    model=Delimitador
    fields = ['del_valor', 'del_codigo']
    def form_valid(self, form):
        return super(DelimitadorCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DelimitadorCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class DelimitadorList(ListView):
    model=Delimitador
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(DelimitadorList, self).get_context_data(**kwargs)
    	lista=Delimitador.objects.all()
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

class DelimitadorDetail(DetailView):
    model=Delimitador

class DelimitadorUpdate(UpdateView):
    model=Delimitador
    fields = ['del_valor','del_codigo']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DelimitadorUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class DelimitadorDelete(DeleteView):
    model=Delimitador
    success_url = reverse_lazy('formato:delimitador_index')

#Clasificacion
class ClasificacionCreate(CreateView):
    model=Clasificacion
    fields = ['for_id','var_id','cla_valor','cla_maximo','cla_minimo']
    def form_valid(self, form):
        return super(ClasificacionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClasificacionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class ClasificacionList(ListView):
    model=Clasificacion
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(ClasificacionList, self).get_context_data(**kwargs)
    	lista=Clasificacion.objects.all()
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

class ClasificacionDetail(DetailView):
    model=Clasificacion

class ClasificacionUpdate(UpdateView):
    model=Clasificacion
    fields = ['for_id','var_id','cla_valor','cla_maximo','cla_minimo']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClasificacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class ClasificacionDelete(DeleteView):
    model=Clasificacion
    success_url = reverse_lazy('formato:clasificacion_index')

#Asociacion
class AsociacionCreate(CreateView):
    model=Asociacion
    fields = ['for_id','dat_id']
    def form_valid(self, form):
        return super(AsociacionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AsociacionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class AsociacionList(ListView):
    model=Asociacion
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(AsociacionList, self).get_context_data(**kwargs)
    	lista=Asociacion.objects.all()
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

class AsociacionDetail(DetailView):
    model=Asociacion

class AsociacionUpdate(UpdateView):
    model=Asociacion
    fields = ['for_id','dat_id']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AsociacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class AsociacionDelete(DeleteView):
    model=Asociacion
    success_url = reverse_lazy('formato:asociacion_index')
