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
    def consultar(self,nombre,marca):
        self.lista=Sensor.objects.filter(sen_nombre=nombre).filter(sen_marca=marca)
        return self.lista
    def filtrar(self,form):
        lista=Sensor.objects.filter(
            sen_nombre=form.cleaned_data['sen_nombre']
        ).filter(
            sen_marca=form.cleaned_data['sen_marca']
        )
        return lista
