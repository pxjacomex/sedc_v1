# -*- coding: utf-8 -*-

from django import forms
from instalacion.models import Instalacion
from estacion.models import Estacion
from datalogger.models import Datalogger


class InstalacionSearchForm(forms.Form):
    def lista_estaciones():
        lista = ()
        lista = lista + (('','----'),)
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_codigo),)
            lista = lista + fila
        return lista
    def lista_datalogger():
        lista = ()
        lista = lista + (('','----'),)
        dataloggers = Datalogger.objects.all()
        for item in dataloggers:
            fila = ((str(item.dat_id),item.dat_serial),)
            lista = lista + fila
        return lista

    Datalogger = forms.ChoiceField(required=False,choices=lista_datalogger())
    Estacion = forms.ChoiceField(required=False,choices=lista_estaciones())

    def filtrar(self,form):
        if form.cleaned_data['Datalogger'] and form.cleaned_data['Estacion']:
            lista=Instalacion.objects.filter(
                dat_id=form.cleaned_data['Datalogger']
            ).filter(
                est_id=form.cleaned_data['Estacion']
            )
        elif form.cleaned_data['Datalogger']  == "" and form.cleaned_data['Estacion']!="":
            lista=Instalacion.objects.filter(
                est_id=form.cleaned_data['Estacion']
            )
        elif form.cleaned_data['Estacion'] == "" and form.cleaned_data['Datalogger']!="":
            lista=Instalacion.objects.filter(
                dat_id=form.cleaned_data['Datalogger']
            )
        else:
            lista=Instalacion.objects.all()
        return lista

    def cadena(self,form):
        keys=form.cleaned_data.keys()
        string=str("?")
        i=1
        for item in keys:
            if i<len(keys):
                string+=item+"="+str(form.cleaned_data[item].encode('utf-8'))+"&"
            else:
                string+=item+"="+str(form.cleaned_data[item])
            i+=1
        return string
