# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Formato, Extension, Delimitador, Clasificacion, Asociacion
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import FormatoSearchForm, ClasificacionSearchForm, AsociacionSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin

#Formato views
class FormatoCreate(LoginRequiredMixin,CreateView):
    model = Formato
    fields = ['ext_id','del_id','mar_id','for_nombre','for_descripcion','for_ubicacion',
              'for_archivo','for_tipo','for_fil_ini','fec_id',
              'for_col_fecha','hor_id','for_col_hora']
    def form_valid(self, form):
        return super(FormatoCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FormatoCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class FormatoList(LoginRequiredMixin,ListView,FormView):
    #parámetros ListView
    model=Formato
    paginate_by=10
    #parámetros FormView
    template_name='formato/formato_list.html'
    form_class=FormatoSearchForm
    #parametros propios
    cadena=str("")
    def get(self, request, *args, **kwargs):
        form=FormatoSearchForm(self.request.GET or None)
        self.object_list=Formato.objects.all()
        if form.is_valid():
            self.object_list=form.filtrar(form)
            self.cadena=form.cadena(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(FormatoList, self).get_context_data(**kwargs)
        page=self.request.GET.get('page')
        print page
        context.update(pagination(self.object_list,page,10))
        context["cadena"]=self.cadena
        return context

class FormatoDetail(LoginRequiredMixin,DetailView):
    model=Formato
    def get_context_data(self, **kwargs):
        context = super(FormatoDetail, self).get_context_data(**kwargs)
        print self.object.for_id
        #variables por formato
        variables=Clasificacion.objects.filter(for_id=self.object.for_id)
        context['variables']=variables
        return context


class FormatoUpdate(LoginRequiredMixin,UpdateView):
    model=Formato
    fields = ['ext_id','del_id','mar_id','for_nombre','for_descripcion','for_ubicacion',
              'for_archivo','for_tipo','for_fil_ini','fec_id',
              'for_col_fecha','hor_id','for_col_hora']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FormatoUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class FormatoDelete(LoginRequiredMixin,DeleteView):
    model=Formato
    success_url = reverse_lazy('formato:formato_index')

#Extension
class ExtensionCreate(LoginRequiredMixin,CreateView):
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

class ExtensionList(LoginRequiredMixin,ListView):
    model=Extension
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(ExtensionList, self).get_context_data(**kwargs)
    	lista=Extension.objects.all()
        page=self.request.GET.get('page')
        context.update(pagination(self.object_list,page,10))
        return context

class ExtensionDetail(LoginRequiredMixin,DetailView):
    model=Extension

class ExtensionUpdate(LoginRequiredMixin,UpdateView):
    model=Extension
    fields = ['ext_valor']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ExtensionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class ExtensionDelete(LoginRequiredMixin,DeleteView):
    model=Extension
    success_url = reverse_lazy('formato:extension_index')

#Delimitador
class DelimitadorCreate(LoginRequiredMixin,CreateView):
    model=Delimitador
    fields = ['del_nombre', 'del_caracter']
    def form_valid(self, form):
        return super(DelimitadorCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DelimitadorCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class DelimitadorList(LoginRequiredMixin,ListView):
    model=Delimitador
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(DelimitadorList, self).get_context_data(**kwargs)
    	lista=Delimitador.objects.all()
        page=self.request.GET.get('page')
    	context.update(pagination(self.object_list,page,10))
        return context

class DelimitadorDetail(LoginRequiredMixin,DetailView):
    model=Delimitador

class DelimitadorUpdate(LoginRequiredMixin,UpdateView):
    model=Delimitador
    fields = ['del_nombre', 'del_caracter']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DelimitadorUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class DelimitadorDelete(LoginRequiredMixin,DeleteView):
    model=Delimitador
    success_url = reverse_lazy('formato:delimitador_index')

#Clasificacion
class ClasificacionCreate(LoginRequiredMixin,CreateView):
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

class ClasificacionList(LoginRequiredMixin,ListView,FormView):
    #parámetros ListView
    model=Clasificacion
    paginate_by=10
    #parámetros FormView
    template_name='formato/clasificacion_list.html'
    form_class=ClasificacionSearchForm
    #parametros propios
    cadena=str("")
    def get(self, request, *args, **kwargs):
        form=ClasificacionSearchForm(self.request.GET or None)
        self.object_list=Clasificacion.objects.all()
        if form.is_valid():
            self.object_list=form.filtrar(form)
            self.cadena=form.cadena(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ClasificacionList, self).get_context_data(**kwargs)
        page=self.request.GET.get('page')
        context.update(pagination(self.object_list,page,10))
        context["cadena"]=self.cadena
        return context

class ClasificacionDetail(LoginRequiredMixin,DetailView):
    model=Clasificacion

class ClasificacionUpdate(LoginRequiredMixin,UpdateView):
    model=Clasificacion
    fields = ['for_id','var_id','cla_valor','cla_maximo','cla_minimo']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClasificacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class ClasificacionDelete(LoginRequiredMixin,DeleteView):
    model=Clasificacion
    success_url = reverse_lazy('formato:clasificacion_index')

#Asociacion
class AsociacionCreate(LoginRequiredMixin,CreateView):
    model=Asociacion
    fields = ['for_id','est_id']
    def form_valid(self, form):
        return super(AsociacionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AsociacionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class AsociacionList(LoginRequiredMixin,ListView):
    #parámetros ListView
    model=Asociacion
    paginate_by=10
    #parámetros FormView
    template_name='formato/asociacion_list.html'
    form_class=AsociacionSearchForm
    #parametros propios
    cadena=str("")
    def get(self, request, *args, **kwargs):
        form=AsociacionSearchForm(self.request.GET or None)
        self.object_list=Asociacion.objects.all()
        if form.is_valid():
            self.object_list=form.filtrar(form)
            self.cadena=form.cadena(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(AsociacionList, self).get_context_data(**kwargs)
        page=self.request.GET.get('page')
        context.update(pagination(self.object_list,page,10))
        context["cadena"]=self.cadena
        return context

class AsociacionDetail(LoginRequiredMixin,DetailView):
    model=Asociacion

class AsociacionUpdate(LoginRequiredMixin,UpdateView):
    model=Asociacion
    fields = ['for_id','est_id']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AsociacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class AsociacionDelete(LoginRequiredMixin,DeleteView):
    model=Asociacion
    success_url = reverse_lazy('formato:asociacion_index')

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
