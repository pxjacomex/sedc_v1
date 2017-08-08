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
from importacion.functions import consultar_formatos

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
            valid,message=procesar_archivo(request.FILES['archivo'],form)
            if valid:
                return HttpResponseRedirect('/importacion/')
            else:
                context={
                    'form':form,
                    'message':message,
                }
                return render(request, 'importacion/importacion_form.html',context)
    else:
        form = UploadFileForm()
    return render(request, 'importacion/importacion_form.html', {'form': form})
#lista de formatos por estacion y datalogger
def lista_formatos(request):
    dat_id=request.GET.get('datalogger',None)
    datos=consultar_formatos(dat_id)
    data={
        'datos':datos,
    }
    return JsonResponse(datos)

"""def subir(request,id):
    importacion=Importacion.objects.get(imp_id=id)
    #print importacion.for_id_id
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
                fecha=fecha_hora.strftime('%Y-%m-%d')
                hora=fecha_hora.strftime('%H:%M')
            for fila in clasificacion:
                variable=Variable.objects.get(var_id=fila['var_id_id'])
                if fila['cla_valor'] is not None:
                    valor=float(valores[fila['cla_valor']])
                else:
                    valor=None
                if fila['cla_maximo'] is not None:
                    maximo=float(valores[fila['cla_maximo']])
                else:
                    maximo=None
                if fila['cla_minimo'] is not None:
                    minimo=float(valores[fila['cla_minimo']])
                else:
                    minimo=None
                print estacion.est_id,variable,fecha,hora,valor,maximo,minimo
                med=Medicion(var_id=variable,est_id=estacion,
                    med_fecha=fecha,med_hora=hora,
                    med_valor=valor,med_maximo=maximo,med_minimo=minimo,
                    med_estado=True)
                med.save()
        i+=1

    return redirect('/importacion/')
#consultar el intervalo de datos por estación"""
