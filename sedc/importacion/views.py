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
    procesar_archivo,guardar_vacios,validar_fechas_archivo)
from importacion.lectura import iniciar_lectura
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin


class ImportacionList(LoginRequiredMixin,ListView):
    model=Importacion
    def get_context_data(self, **kwargs):
        context = super(ImportacionList, self).get_context_data(**kwargs)
        return context

class ImportacionDetail(LoginRequiredMixin,DetailView):
    model=Importacion

class ImportarArchivo(LoginRequiredMixin,FormView):
    template_name='importacion/importacion_form.html'
    form_class=UploadFileForm
    success_url='/importacion/importar/'
    informacion={}
    def post(self, request, *args, **kwargs):
        form=UploadFileForm(request.POST, request.FILES)
        #form=UploadFileForm(self.request.POST)
        if form.is_valid():
            formato=form.cleaned_data['formato']
            estacion=form.cleaned_data['estacion']
            datalogger=form.cleaned_data['datalogger']
            sobreescribir=form.cleaned_data['sobreescribir']
            self.informacion=procesar_archivo(request.FILES['archivo'],form,request)
            if ((self.informacion['valid'] and
                not form.cleaned_data['sobreescribir']) or
                (not self.informacion['valid'] and
                form.cleaned_data['sobreescribir'])):
                if self.informacion['vacio']:
                    self.informacion.update({'form':VaciosForm()})
                return render(request, 'importacion/confirmacion.html',self.informacion)
            '''elif not self.informacion['valid'] and form.cleaned_data['sobreescribir']:
                if self.informacion['vacio']:
                    self.informacion.update({'form':VaciosForm()})
                return render(request, 'importacion/confirmacion.html',self.informacion)'''
        return self.render_to_response(self.get_context_data(form=form))
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
class LeerArchivo(LoginRequiredMixin,FormView):
    template_name='importacion/form.html'
    form_class=FormUpload
    success_url='/importacion/importar/'
    def post(self, request, *args, **kwargs):
        form = FormUpload(request.POST, request.FILES)
        print "llego al post"
        if form.is_valid():
            print "llego al valid"
            if 'archivo' in request.FILES:
                photo = request.FILES['archivo']
                return self.form_valid(form, **kwargs)

            else:
                return self.form_invalid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)


def guardar_archivo(request):
    sobreescribir=request.GET.get('sobreescribir',None)
    with transaction.atomic():
        guardar_datos(sobreescribir)
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
