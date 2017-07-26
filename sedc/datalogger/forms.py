# -*- coding: utf-8 -*-

from django import forms
from datalogger.models import Sensor
class SensorSearchForm(forms.Form):
    TIPO_MARCA=(
        ('CAMPBELL','CAMPBELL'),
        ('VAISALA','VAISALA'),
        ('YOUNG','YOUNG'),
        ('APOGEE','APOGEE'),
        ('TEXAS ELECTRONICS','TEXAS ELECTRONICS'),
        ('HOBO','HOBO'),
    )
    TIPO_NOMBRE=(
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
    sen_nombre = forms.ChoiceField(required=False,choices=TIPO_NOMBRE)
    sen_marca = forms.ChoiceField(required=False,choices=TIPO_MARCA)
    def filtrar(self,form):
        lista=Sensor.objects.filter(
            sen_nombre=form.cleaned_data['sen_nombre']
        ).filter(
            sen_marca=form.cleaned_data['sen_marca']
        )
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
