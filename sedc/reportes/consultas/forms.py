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
    #consulta para agrupar los datos por hora, diario y mes
    def filtrar(self,form):
        #filtrar los datos por estacion, variable y rango de fechas
        consulta=(Medicion.objects
        .filter(est_id=form.cleaned_data['estacion'])
        .filter(var_id=form.cleaned_data['variable'])
        .filter(med_fecha__range=[form.cleaned_data['inicio'],
            form.cleaned_data['fin']]))
        #frecuencia horaria
        if(form.cleaned_data['frecuencia']==str(1)):
            consulta=consulta.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha'),
                hour=ExtractHour('med_hora')
            ).values('year','month','day','hour')
            if(form.cleaned_data['variable']==str(1)):
                consulta=consulta.annotate(valor=Sum('med_valor')).\
                values('valor','year','month','day','hour').\
                order_by('month','day','year','hour')
            else:
                consulta=consulta.annotate(valor=Avg('med_valor')).\
                values('valor','year','month','day','hour').\
                order_by('month','day','year','hour')
        #frecuencia diaria
        elif(form.cleaned_data['frecuencia']==str(2)):
            consulta=consulta.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha')
            ).values('year','month','day')
            if(form.cleaned_data['variable']==str(1)):
                consulta=consulta.annotate(valor=Sum('med_valor')).\
                values('valor','year','month','day').\
                order_by('month','day','year')
            else:
                consulta=consulta.annotate(valor=Avg('med_valor')).\
                values('valor','year','month','day').\
                order_by('month','day','year')
        #frecuencia mensual
        else:
            consulta=consulta.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha')
            ).values('month','year')
            if(form.cleaned_data['variable']==str(1)):
                consulta=consulta.annotate(valor=Sum('med_valor')).\
                values('valor','month','year').\
                order_by('month')
            else:
                consulta=consulta.annotate(valor=Avg('med_valor')).\
                values('valor','month','year').\
                order_by('month')
        return consulta
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
