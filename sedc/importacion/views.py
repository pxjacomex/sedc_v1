# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from importacion.models import Importacion
from vacios.models import Vacios
from django.views.generic import ListView,FormView
from django.views.generic.detail import DetailView
from django.http import JsonResponse

from django.http import HttpResponseRedirect
#from django.shortcuts import render
from importacion.forms import UploadFileForm,VaciosForm,FormUpload
from importacion.functions import (consultar_formatos,guardar_datos,
    guardar_vacios,get_fechas_archivo,validar_fechas)
from importacion.lectura import iniciar_lectura
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from sedc.settings import BASE_DIR
import time
class ImportacionList(LoginRequiredMixin,ListView):
    model=Importacion
    def get_context_data(self, **kwargs):
        context = super(ImportacionList, self).get_context_data(**kwargs)
        return context

class ImportacionDetail(LoginRequiredMixin,DetailView):
    model=Importacion
    def get_context_data(self, **kwargs):
        context = super(ImportacionDetail, self).get_context_data(**kwargs)
        informacion=validar_fechas(self.object)
        context['informacion']=informacion
        return context
class ImportacionCreate(CreateView):
    model = Importacion
    fields = ['est_id','for_id','imp_sobreescribir','imp_archivo']
    def form_valid(self, form):
        archivo=self.request.FILES['imp_archivo']
        form=get_fechas_archivo(archivo,form.instance.for_id,form)
        return super(ImportacionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportacionCreate, self).get_context_data(**kwargs)
        context['title'] = "Subir Archivo"
        return context

class ImportarArchivo(LoginRequiredMixin,FormView):
    template_name='importacion/importacion_form.html'
    form_class=UploadFileForm
    success_url='/importacion/importar/'
    informacion={}
    def get_context_data(self, **kwargs):
        context = super(ImportarArchivo, self).get_context_data(**kwargs)
        if len(self.informacion)>0:
            context['message']=self.informacion['message']
        return context

class GuardarArchivo(LoginRequiredMixin,FormView):
    template_name='importacion/confirmacion.html'
    form_class=VaciosForm
    success_url='/importacion/'
    def post(self, request, *args, **kwargs):
        form=VaciosForm(request.POST or None)
        if form.is_valid():
            guardar_vacios(request,form.cleaned_data['observacion'])
        with transaction.atomic():
            guardar_datos(request)
        return render(request, 'importacion/mensaje.html',{'mensaje':'Informacion Cargada'})

        #return self.render_to_response(self.get_context_data(form=form))
def guardar_archivo(request,imp_id):
    #sobreescribir=request.GET.get('sobreescribir',None)
    #with transaction.atomic():
        #guardar_datos(sobreescribir)
    guardar_datos(imp_id)
    return render(request, 'importacion/mensaje.html',{'mensaje':'Informacion Cargada'})


#lista de formatos por estacion y datalogger
def lista_formatos(request):
    mar_id=request.GET.get('datalogger',None)
    datos=consultar_formatos(mar_id)
    data={
        'datos':datos,
    }
    return JsonResponse(datos)
#lectura automática funcion de prueba
def lectura_automatica(request):
    #iniciar_lectura()
    iniciar_lectura()
    datos={
        'datos':'Lectura Iniciada'
    }
    return JsonResponse(datos)
