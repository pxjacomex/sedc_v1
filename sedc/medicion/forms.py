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
    FRECUENCIA=(
        ('1','Horario'),
        ('2','Diario'),
        ('3','Mensual'),
    )
    estacion=forms.ChoiceField(choices=lista_estaciones())
    variable=forms.ChoiceField(choices=lista_variables())
    #periodo=forms.ChoiceField(choices=lista_year())
    frecuencia=forms.ChoiceField(choices=FRECUENCIA)
    inicio=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Inicio(dd/mm/yyyy)")
    fin=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Fin(dd/mm/yyyy)")
    def filtrar(self,form):
        consulta=(Medicion.objects
        .filter(est_id=form.cleaned_data['estacion'])
        .filter(var_id=form.cleaned_data['variable'])
        #.filter(med_fecha__year=form.cleaned_data['periodo']))
        .filter(med_fecha__range=[form.cleaned_data['inicio'],form.cleaned_data['fin']]))
        #.filter(med_fecha__month=2))
        if(form.cleaned_data['frecuencia']==str(1)):
            consulta=consulta.annotate(time=ExtractHour('med_hora')).values('time')
        elif(form.cleaned_data['frecuencia']==str(2)):
            consulta=consulta.annotate(month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha')).values('month','day')
            if(form.cleaned_data['variable']==str(1)):
                consulta=consulta.annotate(valor=Sum('med_valor')).values('valor','month','day').order_by('month','day')
            else:
                consulta=consulta.annotate(valor=Avg('med_valor')).values('valor','month','day').order_by('month','day')
        else:
            consulta=consulta.annotate(time=ExtractMonth('med_fecha')).values('time')
            if(form.cleaned_data['variable']==str(1)):
                consulta=consulta.annotate(valor=Sum('med_valor')).values('valor','time').order_by('time')
            else:
                consulta=consulta.annotate(valor=Avg('med_valor')).values('valor','time').order_by('time')
        return consulta
