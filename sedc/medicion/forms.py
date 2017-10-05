# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from variable.models import Variable
from medicion.models import Medicion
from django.db.models import Max, Min, Avg, Count,Sum
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)
from datetime import datetime,timedelta,date
class MedicionSearchForm(forms.Form):
    def lista_estaciones():
        lista = ()
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_codigo+str(" ")+item.est_nombre),)
            lista = lista + fila
        return lista
    def lista_variables():
        lista=()
        variables=Variable.objects.all()
        for item in variables:
            fila=((str(item.var_id),item.var_nombre),)
            lista=lista+fila
        return lista
    def lista_year():
        lista=()
        periodos=Medicion.objects.annotate(year=ExtractYear('med_fecha')).values('year').distinct('year')
        for item in periodos:
            fila=((item.get('year'),item.get('year')),)
            lista=lista+fila
        return lista
    TIPO_VARIABLE=(
        ('valor','valor'),
        ('maximo','maximo'),
        ('minimo','minimo'),
    )
    estacion=forms.ChoiceField(choices=lista_estaciones())
    variable=forms.ChoiceField(choices=lista_variables())
    #periodo=forms.ChoiceField(choices=lista_year())
    inicio=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Inicio(dd/mm/yyyy)")
    fin=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Fin(dd/mm/yyyy)")
    #valor=forms.ChoiceField(choices=TIPO_VARIABLE)
class FilterDeleteForm(forms.Form):
    def lista_estaciones():
        lista = ()
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_codigo+str(" ")+item.est_nombre),)
            lista = lista + fila
        return lista
    def lista_variables():
        lista=()
        variables=Variable.objects.all()
        for item in variables:
            fila=((str(item.var_id),item.var_nombre),)
            lista=lista+fila
        return lista
    def lista_year():
        lista=()
        periodos=Medicion.objects.annotate(year=ExtractYear('med_fecha')).values('year').distinct('year')
        for item in periodos:
            fila=((item.get('year'),item.get('year')),)
            lista=lista+fila
        return lista
    TIPO_VARIABLE=(
        ('valor','valor'),
        ('maximo','maximo'),
        ('minimo','minimo'),
    )
    estacion=forms.ChoiceField(choices=lista_estaciones())
    variable=forms.ChoiceField(choices=lista_variables())
    #periodo=forms.ChoiceField(choices=lista_year())
    fec_ini=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Inicio(dd/mm/yyyy)")
    hor_ini=forms.TimeField(input_formats=['%H:%M:%S'],label="Hora de Inicio(HH:MM:SS)")
    fec_fin=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Fin(dd/mm/yyyy)")
    hor_fin=forms.TimeField(input_formats=['%H:%M:%S'],label="Hora de Fin(HH:MM:SS)")
    #valor=forms.ChoiceField(choices=TIPO_VARIABLE)
