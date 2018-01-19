# -*- coding: utf-8 -*-

from django import forms
from estacion.models import Estacion
from medicion.models import Medicion
from variable.models import Variable, Unidad
from cruce.models import Cruce

class AnuarioForm(forms.Form):
    def lista_estaciones():
        lista = ()
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_nombre),)
            lista = lista + fila
        return lista

    ESTACION = lista_estaciones()
    YEAR = (
        ('2007','2007'),
        ('2008','2008'),
        ('2009','2009'),
        ('2010','2010'),
        ('2011','2011'),
        ('2012','2012'),
        ('2016','2016'),
    )
    lista=[]
    estacion = forms.ChoiceField(required=False,choices=ESTACION,label='Estación')
    anio = forms.ChoiceField(required=False,choices=YEAR,label='Año')
class ComparacionForm(forms.Form):
    def lista_estaciones():
        lista = ()
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_codigo),)
            lista = lista + fila
        return lista
    def lista_variables():
        lista=()
        variables=Variable.objects.order_by('var_id').all()
        for item in variables:
            i=((str(item.var_id),item.var_nombre),)
            lista=lista+i
        return lista
    '''favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lista_estaciones(),
    )'''
    FRECUENCIA=(
        ('0','Minima'),
        ('1','5 Minutos'),
        ('2','Horario'),
        ('3','Diario'),
        ('4','Mensual'),
    )
    estacion01 = forms.ChoiceField(
        required=False,
        choices=lista_estaciones(),
        label='Primera Estación')
    estacion02 = forms.ChoiceField(
        required=False,
        choices=lista_estaciones(),
        label='Segunda Estación')
    estacion03 = forms.ChoiceField(
        required=False,
        choices=lista_estaciones(),
        label='Tercera Estación')
    variable=forms.ChoiceField(choices=lista_variables())
    inicio=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Inicio(dd/mm/yyyy)")
    fin=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Fin(dd/mm/yyyy)")
    frecuencia=forms.ChoiceField(choices=FRECUENCIA)
