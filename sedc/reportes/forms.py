# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from estacion.models import Estacion
from medicion.models import Medicion
from variable.models import Variable, Unidad
from cruce.models import Cruce

class AnuarioForm(ModelForm):
    '''def lista_estaciones():
        lista = ()
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_nombre),)
            lista = lista + fila
        return lista'''
    class Meta:
        model=Estacion
        fields=['est_id']
    #ESTACION = lista_estaciones()
    YEAR = (
        ('2007','2007'),
        ('2008','2008'),
        ('2009','2009'),
        ('2010','2010'),
        ('2011','2011'),
        ('2012','2012'),
        ('2016','2016'),
        ('2017','2017'),
    )
    lista=[]
    #estacion = forms.ChoiceField(required=False,choices=ESTACION,label='Estación')
    estacion = forms.ModelChoiceField(required=False,
        queryset=Estacion.objects.order_by('est_id').all(),label='Estación')
    anio = forms.ChoiceField(required=False,choices=YEAR,label='Año')
class ComparacionForm(forms.Form):
    UNIDADES=(
        ('0','Horario'),
        ('1','Diaria'),
        ('2','Mensual'),
        ('3','Anual'),
    )
    estacion01 = forms.ModelChoiceField(required=False,
        queryset=Estacion.objects.order_by('est_id').all(),label='Estación 01')
    estacion02 = forms.ModelChoiceField(required=False,
        queryset=Estacion.objects.order_by('est_id').all(),label='Estación 02')
    estacion03 = forms.ModelChoiceField(required=False,
        queryset=Estacion.objects.order_by('est_id').all(),label='Estación 03')
    variable = forms.ModelChoiceField(required=False,
        queryset=Variable.objects.order_by('var_id').all(),label='Variable')
    inicio=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Inicio(dd/mm/yyyy)")
    fin=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Fin(dd/mm/yyyy)")
    tiempo=forms.IntegerField(max_value=60,min_value=5,label="Tiempo en Minutos",help_text="Valor entre 5 y 60")
    #frecuencia=forms.ChoiceField(choices=UNIDADES,label="Frecuencia")
