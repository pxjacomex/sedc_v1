# -*- coding: utf-8 -*-

from django import forms
from cruce.models import Cruce
from estacion.models import Estacion
from variable.models import Variable


class CruceSearchForm(forms.Form):
    def lista_estaciones():
        lista = ()
        lista = lista + (('','----'),)
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_codigo),)
            lista = lista + fila
        return lista
    def lista_variable():
        lista = ()
        lista = lista + (('','----'),)
        variable = Variable.objects.all()
        for item in variable:
            fila = ((str(item.var_id),item.var_nombre),)
            lista = lista + fila
        return lista

    Variable = forms.ChoiceField(required=False,choices=lista_variable())
    Estacion = forms.ChoiceField(required=False,choices=lista_estaciones())

    def filtrar(self,form):
        if form.cleaned_data['Variable'] and form.cleaned_data['Estacion']:
            lista=Cruce.objects.filter(
                var_id=form.cleaned_data['Variable']
            ).filter(
                est_id=form.cleaned_data['Estacion']
            )
        elif form.cleaned_data['Variable']  == "":
            lista=Cruce.objects.filter(
                est_id=form.cleaned_data['Estacion']
            )
        elif form.cleaned_data['Estacion'] == "":
            lista=Cruce.objects.filter(
                var_id=form.cleaned_data['Varible']
            )
        else:
            lista=Cruce.objects.all()
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
