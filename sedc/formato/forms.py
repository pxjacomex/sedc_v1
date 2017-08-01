# -*- coding: utf-8 -*-

from django import forms
from formato.models import Formato, Variable, Clasificacion

class FormatoSearchForm(forms.Form):

    lista=[]
    Descripcion = forms.CharField(required=False,max_length=100)

    def filtrar(self,form):
        if form.cleaned_data['Descripcion'] != "":
            lista=Formato.objects.filter(
                for_descripcion__icontains=form.cleaned_data['Descripcion']
            )
        else:
            lista=Formato.objects.all()
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


class ClasificacionSearchForm(forms.Form):
    def lista_formato():
        lista = ()
        lista = lista + (('','----'),)
        formato = Formato.objects.all()
        for item in formato:
            fila = ((str(item.for_id),item.for_descripcion),)
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
    Formato = forms.ChoiceField(required=False,choices=lista_formato())

    def filtrar(self,form):
        if form.cleaned_data['Variable'] and form.cleaned_data['Formato'] != "":
            lista=Clasificacion.objects.filter(
                var_id=form.cleaned_data['Variable']
            ).filter(
                for_id=form.cleaned_data['Formato']
            )
        elif form.cleaned_data['Variable'] == "":
            lista=Clasificacion.objects.filter(
                for_id=form.cleaned_data['Formato']
            )
        elif form.cleaned_data['Formato'] == "":
            lista=Clasificacion.objects.filter(
                var_id=form.cleaned_data['Variable']
            )
        else:
            lista=Clasificacion.objects.all()
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
