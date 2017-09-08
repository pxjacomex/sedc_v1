from django import forms
from estacion.models import Estacion
from variable.models import Variable
from medicion.models import Medicion
from django.db.models import Max, Min, Avg, Count,Sum
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)
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
    def filtrar(self,form):
        consulta=(Medicion.objects
        .filter(est_id=form.cleaned_data['estacion'])
        .filter(var_id=form.cleaned_data['variable'])
        .filter(med_fecha__range=[form.cleaned_data['inicio'],form.cleaned_data['fin']]))
        variable=Variable.objects.get(var_id=form.cleaned_data['variable'])
        i=0
        ans=0
        datos=[]
        for item in consulta:
            obj_analisis =Analisis()
            valor=item.med_valor
            valor_error=False
            resta=0
            resta_error=False
            if valor<variable.var_minimo or valor>variable.var_maximo:
                valor_error=True
            if i==0:
                resta=0
                ans=valor
            else:
                resta=valor-ans
                ans=valor
            i+=1
            if resta<variable.var_sos:
                resta_error="normal"
            elif resta>=variable.var_sos and resta<variable.var_err:
                resta_error="sospechoso"
            else:
                resta_error="error"
            obj_analisis.iden=item.med_id
            obj_analisis.fecha=item.med_fecha
            obj_analisis.hora=item.med_hora
            obj_analisis.valor=item.med_valor
            obj_analisis.valor_error=valor_error
            obj_analisis.resta=abs(resta)
            obj_analisis.resta_error=resta_error
            datos.append(obj_analisis)

        return datos
    def datos_variable(self,form):
        variable=Variable.objects.get(var_id=form.cleaned_data['variable'])
        return variable
class Analisis(object):
    iden=0
    fecha=""
    hora=""
    valor=0
    valor_error=False
    resta=0
    resta_error="Normal"
