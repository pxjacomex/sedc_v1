# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from importacion.models import Importacion
from formato.models import Formato,Clasificacion,Delimitador
from estacion.models import Estacion
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
import time
from datetime import datetime
from django.conf import settings
class ImportacionCreate(CreateView):
    model=Importacion
    fields = ['est_id','for_id','imp_archivo','imp_sobreescribir']
    def form_valid(self, form):
        #agregar valor al campo created_by
        form.instance.imp_fecha = time.strftime('%Y-%m-%d')
        form.instance.imp_hora = time.strftime('%H:%M')
        return super(ImportacionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ImportacionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Subir"
        return context

class ImportacionList(ListView):
    model=Importacion
    def get_context_data(self, **kwargs):
        context = super(ImportacionList, self).get_context_data(**kwargs)
        return context

class ImportacionDetail(DetailView):
    model=Importacion
def subir(request,id):
    importacion=Importacion.objects.get(imp_id=id)
    print importacion.for_id_id
    formato=Formato.objects.get(for_id=importacion.for_id_id)
    estacion=Estacion.objects.get(est_id=importacion.est_id_id)
    clasificacion=list(Clasificacion.objects.filter(
        for_id=formato.for_id).values())
    ubicacion=settings.BASE_DIR+importacion.imp_archivo.url
    #print ubicacion
    #print formato.del_id_id
    delimitador=Delimitador.objects.get(del_id=formato.del_id_id)
    archivo=open(ubicacion,'r')
    i=1
    for linea in archivo.readlines():
        #controlar la fila de inicio
        if i>=formato.for_fil_ini:
            valores=linea.split(delimitador.del_caracter)
            if formato.for_col_hora==formato.for_col_hora:
                fecha_hora=datetime.strptime(valores[formato.for_col_hora], formato.for_fecha+str(" ")+formato.for_hora)
                fecha=fecha_hora.strftime("%Y-%m-%d")
                hora=fecha_hora.strftime("%H:%M:%S")
            for fila in clasificacion:
                var_id=fila['var_id_id']
                if fila['cla_valor'] is not None:
                    valor=linea[fila['cla_valor']]
                if fila['cla_maximo'] is not None:
                    maximo=linea[fila['cla_maximo']]
                if fila['cla_minimo'] is not None:
                    minimo=linea[fila['cla_minimo']]
                    

        i+=1
    return redirect('/importacion/')
