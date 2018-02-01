# -*- coding: utf-8 -*-

from django.forms import ModelForm
from variable.models import Control
from estacion.models import Estacion
from formato.models import Variable
#from sensor.models import Sensor

class ControlSearchForm(ModelForm):
    class Meta:
        model=Control
        fields=['var_id','est_id']
    lista=[]


    def filtrar(self,form):
        var_id=form.cleaned_data['var_id']
        est_id=form.cleaned_data['est_id']
        sen_id=form.cleaned_data['est_id']
        if var_id and est_id and sen_id:
            lista=Control.objects.filter(
                var_id=var_id
            ).filter(
                est_id=est_id
            ).filter(
                sen_id=sen_id
            )
        elif var_id is None and est_id is None:
            lista=Control.objects.filter(
                sen_id=sen_id
            )
        elif var_id is None and sen_id is None:
            print est_id
            lista=Control.objects.filter(
                est_id=est_id
            )
        elif est_id is None and sen_id is None:
            lista=Control.objects.filter(
                var_id=var_id
            )
        elif var_id is None:
            lista=Control.objects.filter(
                est_id=est_id
            ).filter(
                sen_id=sen_id
            )
        elif est_id is None:
            lista=Control.objects.filter(
                var_id=var_id
            ).filter(
                sen_id=sen_id
            )
        elif sen_id is None:
            lista=Control.objects.filter(
                var_id=var_id
            ).filter(
                est_id=est_id
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
                string+=item+"="+str(form.cleaned_data[item])+"&"
            else:
                string+=item+"="+str(form.cleaned_data[item])
            i+=1
        return string
