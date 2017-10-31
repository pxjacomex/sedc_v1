# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from bitacora.models import Bitacora
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from bitacora.forms import BitacoraSearchForm

#bitacora views
class BitacoraCreate(CreateView):
    model=Bitacora
    fields = ['bit_id','est_id','var_id','bit_fecha_ini','bit_fecha_fin','bit_observacion']
    def form_valid(self, form):
        return super(BitacoraCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BitacoraCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class BitacoraList(ListView,FormView):
    model=Bitacora
    paginate_by = 10
    template_name='bitacora/bitacora_list.html'
    form_class=BitacoraSearchForm
    #parametros propios
    cadena=str("")
    def get(self, request, *args, **kwargs):
        form=BitacoraSearchForm(self.request.GET or None)
        self.object_list=Bitacora.objects.all()
        if form.is_valid():
            self.object_list=form.filtrar(form)
            self.cadena=form.cadena(form)
        return self.render_to_response(self.get_context_data(form=form))

class BitacoraDetail(DetailView):
    model=Bitacora

class BitacoraUpdate(UpdateView):
    model=Bitacora
    fields = ['bit_id','est_id','var_id','bit_fecha_ini','bit_fecha_fin','bit_observacion']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BitacoraUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class BitacoraDelete(DeleteView):
    model=Bitacora
    success_url = reverse_lazy('bitacora:bitacora_index')
