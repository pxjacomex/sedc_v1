# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from instalacion.models import Instalacion
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from instalacion.forms import InstalacionSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
#Variable views
class InstalacionCreate(LoginRequiredMixin,CreateView):
    model=Instalacion
    fields = ['ins_id','est_id','dat_id','ins_fecha_ini','ins_fecha_fin','ins_en_uso','ins_observacion']
    def form_valid(self, form):
        return super(InstalacionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InstalacionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class InstalacionList(LoginRequiredMixin,ListView,FormView):
    model=Instalacion
    paginate_by = 10
    template_name='instalacion/instalacion_list.html'
    form_class=InstalacionSearchForm
    #parametros propios
    cadena=str("")
    def get(self, request, *args, **kwargs):
        form=InstalacionSearchForm(self.request.GET or None)
        self.object_list=Instalacion.objects.all()
        if form.is_valid():
            self.object_list=form.filtrar(form)
            self.cadena=form.cadena(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(InstalacionList, self).get_context_data(**kwargs)
        page=self.request.GET.get('page')
        print kwargs
        context.update(pagination(self.object_list,page,10))
        context["cadena"]=self.cadena
        return context

class InstalacionDetail(LoginRequiredMixin,DetailView):
    model=Instalacion

class InstalacionUpdate(LoginRequiredMixin,UpdateView):
    model=Instalacion
    fields = ['ins_id','est_id','dat_id','ins_fecha_ini','ins_fecha_fin','ins_en_uso','ins_observacion']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InstalacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class InstalacionDelete(LoginRequiredMixin,DeleteView):
    model=Instalacion
    success_url = reverse_lazy('instalacion:instalacion_index')
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
