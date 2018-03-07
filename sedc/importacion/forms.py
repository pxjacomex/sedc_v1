# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from medicion.models import Medicion
from variable.models import Variable
from datalogger.models import Datalogger
from marca.models import Marca
from datetime import datetime,timedelta
from formato.models import Formato
from importacion.models import Importacion
class UploadFileForm(forms.Form):
    estacion=forms.ModelChoiceField(queryset=Estacion.objects.all())
    datalogger=forms.ModelChoiceField(queryset=Marca.objects.all())
    formato=forms.ModelChoiceField(
        queryset=Formato.objects.order_by('for_id').all())
    sobreescribir=forms.BooleanField(required=False)
    archivo = forms.FileField()

class FormUpload(forms.Form):
    estacion=forms.ModelChoiceField(queryset=Estacion.objects.all())
    datalogger=forms.ModelChoiceField(queryset=Marca.objects.all())
    formato=forms.ModelChoiceField(
        queryset=Formato.objects.order_by('for_id').all())
    sobreescribir=forms.BooleanField(required=False)
    archivo = forms.FileField()
    def __init__(self, *args, **kwargs):
        super(FormUpload, self).__init__(*args, **kwargs)
class VaciosForm(forms.Form):
    observacion=forms.CharField(widget=forms.Textarea)
