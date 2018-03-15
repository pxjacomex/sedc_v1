# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from registro.models import LogMedicion,LogMedicionSearchForm
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView

from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class LogMedicionList(LoginRequiredMixin,ListView,FormView):
    #parámetros ListView
    model=LogMedicion
    paginate_by=10
    #parámetros FormView
    template_name='registro/registro_list.html'
    form_class=LogMedicionSearchForm
    #parametros propios
    cadena=str("")
    def get(self, request, *args, **kwargs):
        form=LogMedicionSearchForm(self.request.GET or None)
        self.object_list=Estacion.objects.all()
        if form.is_valid():
            self.object_list=form.filtrar(form)
            self.cadena=form.cadena(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(LogMedicionList, self).get_context_data(**kwargs)
        page=self.request.GET.get('page')
        context.update(pagination(self.object_list,page,10))
        context["cadena"]=self.cadena
        return context
