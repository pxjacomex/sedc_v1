# -*- coding: utf-8 -*-

from django import forms
'''from sensor.models import Sensor
from marca.models import Marca

class SensorSearchForm(forms.Form):
    class Meta:
        model=Sensor
        fields=['sen_nombre','mar_id']
    def filtrar(self,form):
        sen_nombre=form.cleaned_data['sen_nombre']
        mar_id=form.cleaned_data['mar_id']
        #filtra los resultados en base al form
        if sen_nombre and mar_id:
            lista=Sensor.objects.filter(
                sen_nombre=sen_nombre
            ).filter(
                mar_id=mar_id
            )

        elif sen_nombre is None and mar_id:
            lista=Sensor.objects.filter(
                mar_id=mar_id
            )
        elif mar_id is None and sen_nombre:
            lista=Sensor.objects.filter(
                sen_nombre=sen_nombre
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
                string+=item+"="+str(form.cleaned_data[item])+"&"
            else:
                string+=item+"="+str(form.cleaned_data[item])
            i+=1
        return string'''
