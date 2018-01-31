# -*- coding: utf-8 -*-

from django.forms import ModelForm
from datalogger.models import Datalogger#, Sensor
from marca.models import Marca

class DataloggerSearchForm(ModelForm):
    class Meta:
        model=Datalogger
        fields=['mar_id','dat_modelo']
    lista=[]

    def filtrar(self,form):
        mar_id=form.cleaned_data['mar_id']
        dat_modelo=form.cleaned_data['dat_modelo']
        #filtra los resultados en base al form
        if mar_id and dat_modelo:
            lista=Datalogger.objects.filter(
                mar_id=mar_id
            ).filter(
                dat_modelo=dat_modelo
            )
        elif mar_id is None and dat_modelo:
            lista=Datalogger.objects.filter(
                dat_modelo__icontains=dat_modelo
            )
        elif dat_modelo is None and mar_id:
            lista=Datalogger.objects.filter(
                mar_id=mar_id
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
                string+=item+"="+str(form.cleaned_data[item])+"&"
            else:
                string+=item+"="+str(form.cleaned_data[item])
            i+=1
        return string
