# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from importacion.models import Importacion

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse


from django.http import HttpResponseRedirect
#from django.shortcuts import render
from importacion.forms import UploadFileForm, procesar_archivo
from importacion.functions import consultar_formatos,guardar_datos

from django.db import transaction

class ImportacionList(ListView):
    model=Importacion
    def get_context_data(self, **kwargs):
        context = super(ImportacionList, self).get_context_data(**kwargs)
        return context

class ImportacionDetail(DetailView):
    model=Importacion
def importar_archivo(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            informacion=procesar_archivo(request.FILES['archivo'],form,request)
            informacion['form']=form
            if informacion['valid'] and not form.cleaned_data['sobreescribir']:
                return render(request, 'importacion/confirmacion.html',informacion)
            elif not informacion['valid'] and form.cleaned_data['sobreescribir']:
                return render(request, 'importacion/confirmacion.html',informacion)
            elif informacion['valid'] and form.cleaned_data['sobreescribir']:
                context={
                    'form':form,
                    'message':informacion['message'],
                }
                return render(request, 'importacion/importacion_form.html',context)
            else:
                context={
                    'form':form,
                    'message':informacion['message'],
                }
                return render(request, 'importacion/importacion_form.html',context)
    else:
        form = UploadFileForm()
    return render(request, 'importacion/importacion_form.html', {'form': form})
def guardar_archivo(request):
    '''if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            sobreescribir=form.cleaned_data['sobreescribir']'''
    sobreescribir=request.GET.get('sobreescribir',None)
    with transaction.atomic():
        guardar_datos(sobreescribir,request)
    return render(request, 'importacion/mensaje.html',{'mensaje':'Informacion Cargada'})

#lista de formatos por estacion y datalogger
def lista_formatos(request):
    mar_id=request.GET.get('datalogger',None)
    datos=consultar_formatos(mar_id)
    data={
        'datos':datos,
    }
    return JsonResponse(datos)
