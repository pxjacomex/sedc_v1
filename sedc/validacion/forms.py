# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from variable.models import Variable

class ValidacionProcess(forms.Form):
    def lista_estaciones():
        lista = ()
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_codigo+str(" ")+item.est_nombre),)
            lista = lista + fila
        return lista
    def lista_variables():
        lista = ()
        variables = Variable.objects.all()
        for item in variables:
            fila = ((str(item.var_id),item.var_nombre),)
            lista = lista + fila
        return lista
    estacion=forms.ChoiceField(choices=lista_estaciones())
    variable=forms.ChoiceField(choices=lista_variables)
    #inicio=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Inicio(dd/mm/yyyy)")
    #fin=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Fin(dd/mm/yyyy)")
