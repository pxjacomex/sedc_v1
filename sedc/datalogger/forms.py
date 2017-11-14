# -*- coding: utf-8 -*-

from django import forms
from datalogger.models import Datalogger#, Sensor
from marca.models import Marca

class DataloggerSearchForm(forms.Form):
    def lista_marcas():
        lista=()
        lista = lista + (('','----'),)
        marcas=Marca.objects.all()
        for item in marcas:
            fila=((str(item.mar_id),item.mar_nombre),)
            lista=lista+fila
        return lista
    lista=[]
    Marca = forms.ChoiceField(required=False,choices=lista_marcas())
    Modelo = forms.CharField(required=False,max_length=25)

    def filtrar(self,form):
        #filtra los resultados en base al form
        if form.cleaned_data['Marca'] and form.cleaned_data['Modelo']:
            lista=Datalogger.objects.filter(
                mar_id=form.cleaned_data['Marca']
            ).filter(
                dat_modelo=form.cleaned_data['Modelo']
            )
        elif form.cleaned_data['Marca'] == "" and form.cleaned_data['Modelo']!="":
            lista=Datalogger.objects.filter(
                dat_modelo=form.cleaned_data['Modelo']
            )
        elif form.cleaned_data['Modelo'] == "" and form.cleaned_data['Marca']!="":
            lista=Datalogger.objects.filter(
                mar_id=form.cleaned_data['Marca']
            )
        else:
            lista=Datalogger.objects.all()
        return lista

    def cadena(self,form):
        #forma cadena de url
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

"""class SensorSearchForm(forms.Form):
    def lista_marcas():
        lista=()
        lista = lista + (('','----'),)
        marcas=Marca.objects.all()
        for item in marcas:
            fila=((str(item.mar_id),item.mar_nombre),)
            lista=lista+fila
        return lista
    TIPO_NOMBRE=(
        ('','----'),
        ('Termómetro','Termómetro'),
        ('Higrómetro','Higrómetro'),
        ('Pluviógrafo','Pluviógrafo'),
        ('Veleta','Veleta'),
        ('Anemómetro','Anemómetro'),
        ('Barómetro','Barómetro'),
        ('TDR','TDR'),
        ('Piranómetro','Piranómetro'),
        ('Termómetro de agua','Termómetro de agua'),
        ('Sensor de nivel','Sensor de nivel'),
    )
    lista=[]
    Nombre = forms.ChoiceField(required=False,choices=TIPO_NOMBRE)
    Marca = forms.ChoiceField(required=False,choices=lista_marcas())

    def filtrar(self,form):
        #filtra los resultados en base al form
        if form.cleaned_data['Nombre'] and form.cleaned_data['Marca']:
            lista=Sensor.objects.filter(
                sen_nombre=form.cleaned_data['Nombre']
            ).filter(
                mar_id=form.cleaned_data['Marca']
            )
        elif form.cleaned_data['Nombre'] == "":
            lista=Sensor.objects.filter(
                mar_id=form.cleaned_data['Marca']
            )
        elif form.cleaned_data['Marca'] == "":
            lista=Sensor.objects.filter(
                sen_nombre=form.cleaned_data['Nombre']
            )
        else:
            lista=Sensor.objects.all()
        return lista

    def cadena(self,form):
        #forma cadena de url
        keys=form.cleaned_data.keys()
        string=str("?")
        i=1
        for item in keys:
            if i<len(keys):
                string+=item+"="+str(form.cleaned_data[item].encode('utf-8'))+"&"
            else:
                string+=item+"="+str(form.cleaned_data[item].encode('utf-8'))
            i+=1
        return string"""
