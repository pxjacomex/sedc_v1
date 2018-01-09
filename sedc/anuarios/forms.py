# -*- coding: utf-8 -*-

from django import forms
from estacion.models import Estacion
from variable.models import Variable
class AnuarioForm(forms.Form):
    def lista_estaciones():
        lista = ()
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_codigo + str(" ") + item.est_nombre),)
            lista = lista + fila
        return lista
    def lista_variables():
        lista = ()
        variables = Variable.objects.all()
        for item in variables:
            fila = ((str(item.var_id),item.var_nombre),)
            lista = lista + fila
        return lista

    YEAR = (
        ('2007','2007'),
        ('2008','2008'),
        ('2009','2009'),
        ('2010','2010'),
        ('2011','2011'),
        ('2012','2012'),
        ('2013','2013'),
        ('2012','2014'),
        ('2015','2015'),
        ('2016','2016'),
    )

    estacion = forms.ChoiceField(required=False,choices=lista_estaciones(),label='Estación')
    variable = forms.ChoiceField(required=False,choices=lista_variables(),label='Variable')
    periodo = forms.ChoiceField(required=False,choices=YEAR,label='Año')
