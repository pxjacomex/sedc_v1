# -*- coding: utf-8 -*-

from django import forms
from estacion.models import Estacion
from medicion.models import Medicion
from reportes.typeI import TypeI
from reportes.typeII import TypeII
from reportes.typeIII import TypeIII
from reportes.typeIV import TypeIV
from reportes.typeV import TypeV
from reportes.typeVI import TypeVI

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

    def filtrar(self,form):
        context = {}

        typeI = [6,8,9,10,11]
        typeII = [1]
        typeIII = [2]
        typeIV = [3]
        typeV = [4,5]
        typeVI = [7]

        variables = list(Medicion.objects.filter(est_id=form.cleaned_data['estacion']).filter(med_fecha__year=form.cleaned_data['anio']).values('var_id_id').distinct('var_id_id').order_by('var_id_id'))

        obj_typeI=TypeI()
        obj_typeII=TypeII()
        obj_typeIII=TypeIII()
        obj_typeIV=TypeIV()
        obj_typeV=TypeV()
        obj_typeVI=TypeVI()

        for item in variables:
            '''if item.get('var_id_id') in typeI:
                matriz = obj_typeI.matriz(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                grafico = obj_typeI.grafico(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                context.update({str(item.get('var_id_id')) + '_grafico': grafico})

            elif item.get('var_id_id') in typeII:
                matriz = obj_typeII.matriz(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                grafico = obj_typeII.grafico(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                context.update({str(item.get('var_id_id')) + '_grafico': grafico})'''

            if item.get('var_id_id') in typeIII:
                matriz = obj_typeIII.matriz(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                #grafico = obj_typeIII.grafico(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                #context.update({str(item.get('var_id_id')) + '_grafico': grafico})

            '''elif item.get('var_id_id') in typeIV:
                matriz = obj_typeIV.matriz(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                grafico = obj_typeIV.grafico(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                context.update({str(item.get('var_id_id')) + '_grafico': grafico})

            elif item.get('var_id_id') in typeV:
                matriz = obj_typeV.matriz(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                #context.update({str(item.get('var_id_id')) + '_grafico': grafico})

            elif item.get('var_id_id') in typeVI:
                matriz = obj_typeVI.matriz(form.cleaned_data['estacion'],str(item.get('var_id_id')),form.cleaned_data['anio'])
                #grafico = obj_typeVI.grafico(form.cleaned_data['estacion'],item.get('var_id_id'),form.cleaned_data['anio'])
                context.update({str(item.get('var_id_id')) + '_matriz': matriz})
                #context.update({str(item.get('var_id_id')) + '_grafico': grafico})'''

        return context
