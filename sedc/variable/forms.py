# -*- coding: utf-8 -*-

from django import forms
from variable.models import Control
from estacion.models import Estacion
from formato.models import Variable
from datalogger.models import Sensor

class ControlSearchForm(forms.Form):
    def lista_estaciones():
        lista = ()
        lista = lista + (('','----'),)
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_codigo),)
            lista = lista + fila
        return lista
    def lista_variables():
        lista=()
        lista = lista + (('','----'),)
        variables=Variable.objects.all()
        for item in variables:
            fila=((str(item.var_id),item.var_nombre),)
            lista=lista+fila
        return lista
    def lista_sensores():
        lista=()
        lista = lista + (('','----'),)
        sensores=Sensor.objects.all()
        for item in sensores:
            fila=((str(item.sen_id),item.sen_nombre + " " + item.sen_modelo + " " + item.sen_serial),)
            lista=lista+fila
        return lista

    lista=[]
    Variable = forms.ChoiceField(required=False,choices=lista_variables())
    Estacion = forms.ChoiceField(required=False,choices=lista_estaciones())
    Sensor = forms.ChoiceField(required=False,choices=lista_sensores())


    def filtrar(self,form):
        if form.cleaned_data['Variable'] and form.cleaned_data['Estacion'] and form.cleaned_data['Sensor']:
            lista=Control.objects.filter(
                var_id=form.cleaned_data['Variable']
            ).filter(
                est_id=form.cleaned_data['Estacion']
            ).filter(
                sen_id=form.cleaned_data['Sensor']
            )
        elif form.cleaned_data['Variable'] == "" and form.cleaned_data['Estacion'] == "":
            lista=Control.objects.filter(
                sen_id=form.cleaned_data['Sensor']
            )
        elif form.cleaned_data['Variable'] == "" and form.cleaned_data['Sensor'] == "":
            print form.cleaned_data['Estacion']
            lista=Control.objects.filter(
                est_id=form.cleaned_data['Estacion']
            )
        elif form.cleaned_data['Estacion'] == "" and form.cleaned_data['Sensor'] == "":
            lista=Control.objects.filter(
                var_id=form.cleaned_data['Variable']
            )
        elif form.cleaned_data['Variable']  == "":
            lista=Control.objects.filter(
                est_id=form.cleaned_data['Estacion']
            ).filter(
                sen_id=form.cleaned_data['Sensor']
            )
        elif form.cleaned_data['Estacion'] == "":
            lista=Control.objects.filter(
                var_id=form.cleaned_data['Variable']
            ).filter(
                sen_id=form.cleaned_data['Sensor']
            )
        elif form.cleaned_data['Sensor'] == "":
            lista=Control.objects.filter(
                var_id=form.cleaned_data['Variable']
            ).filter(
                est_id=form.cleaned_data['Estacion']
            )
        else:
            lista=Control.objects.all()
        return lista

    def cadena(self,form):
        keys=form.cleaned_data.keys()
        string=str("?")
        i=1
        for item in keys:
            if i<len(keys):
                string+=item+"="+str(form.cleaned_data[item].encode('utf-8'))+"&"
            else:
                string+=item+"="+str(form.cleaned_data[item].encode('utf-8'))
            i+=1
        return string
