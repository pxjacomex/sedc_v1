# -*- coding: utf-8 -*-

from django import forms
from frecuencia.models import Frecuencia
from estacion.models import Estacion
from formato.models import Variable

class FrecuenciaSearchForm(forms.Form):
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

    lista=[]
    Variable = forms.ChoiceField(required=False,choices=lista_variables())
    Estacion = forms.ChoiceField(required=False,choices=lista_estaciones())
    #Fecha = forms.DateField(required=False,input_formats=['%d/%m/%Y'],label="Fecha (dd/mm/yyyy)")

    def filtrar(self,form):
        if form.cleaned_data['Variable'] and form.cleaned_data['Estacion']:
            lista=Frecuencia.objects.filter(
                var_id=form.cleaned_data['Variable']
            ).filter(
                est_id=form.cleaned_data['Estacion']
            )
        elif form.cleaned_data['Variable']  == "" and form.cleaned_data['Estacion']!="":
            lista=Frecuencia.objects.filter(
                est_id=form.cleaned_data['Estacion']
            )
        elif form.cleaned_data['Estacion'] == "" and form.cleaned_data['Variable']!="":
            lista=Frecuencia.objects.filter(
                var_id=form.cleaned_data['Variable']
            )
        else:
            lista=Frecuencia.objects.all()
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
