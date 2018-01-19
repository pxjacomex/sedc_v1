# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from variable.models import Variable, Unidad
from medicion.models import Medicion
from django.db.models import Max, Min, Avg, Count,Sum
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)
import plotly.offline as opy
import plotly.graph_objs as go
import datetime, calendar

from django.db import connection
#cursor = connection.cursor()

class MedicionSearchForm(forms.Form):
    def lista_estaciones():
        lista = ()
        estaciones = Estacion.objects.all()
        for item in estaciones:
            i = ((str(item.est_id),item.est_codigo+str(" ")+item.est_nombre),)
            lista = lista + i
        return lista
    def lista_variables():
        lista=()
        variables=Variable.objects.order_by('var_id').all()
        for item in variables:
            i=((str(item.var_id),item.var_nombre),)
            lista=lista+i
        return lista
    def lista_year():
        lista=()
        periodos=Medicion.objects.annotate(year=ExtractYear('med_fecha')).values('year').distinct('year')
        for item in periodos:
            i=((item.get('year'),item.get('year')),)
            lista=lista+i
        return lista
    FRECUENCIA=(
        ('0','Crudo'),
        ('1','5 Minutos'),
        ('2','Horario'),
        ('3','Diario'),
        ('4','Mensual'),
    )
    estacion=forms.ChoiceField(choices=lista_estaciones())
    variable=forms.ChoiceField(choices=lista_variables())
    frecuencia=forms.ChoiceField(choices=FRECUENCIA)
    inicio=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Inicio(dd/mm/yyyy)")
    fin=forms.DateField(input_formats=['%d/%m/%Y'],label="Fecha de Fin(dd/mm/yyyy)")
    #saber si hay datos
    def exists(self,form):
        #print self.estacion
        estacion=form.cleaned_data['estacion']
        variable=form.cleaned_data['variable']
        fecha_inicio=form.cleaned_data['inicio']
        fecha_fin=form.cleaned_data['fin']
        frecuencia=form.cleaned_data['frecuencia']
        #filtrar los datos por estacion, variable y rango de fechas
        consulta=(Medicion.objects.filter(est_id=estacion)
        .filter(var_id=variable)
        .filter(med_fecha__range=[fecha_inicio,fecha_fin]).exists())
        print consulta
        return consulta


    #consulta para agrupar los datos por hora, diario y mes
    def filtrar(self,form):
        #filtrar los datos por estacion, variable y rango de fechas
        estacion=form.cleaned_data['estacion']
        variable=form.cleaned_data['variable']
        fecha_inicio=form.cleaned_data['inicio']
        fecha_fin=form.cleaned_data['fin']
        frecuencia=form.cleaned_data['frecuencia']
        #filtrar los datos por estacion, variable y rango de fechas
        consulta=(Medicion.objects.filter(est_id=estacion)
        .filter(var_id=variable).filter(med_fecha__range=[fecha_inicio,fecha_fin]))

        #frecuencia instantanea
        if(frecuencia==str(0)):
            datos=list(consulta.values('med_valor','med_maximo','med_minimo'
                ,'med_fecha','med_hora').order_by('med_fecha','med_hora'))
        #cada 5 min
        elif(frecuencia==str(1)):
            if variable==str(1):
                with connection.cursor() as cursor:
                    cursor.execute("SELECT sum(med_valor) as valor, \
                        to_timestamp(floor((extract('epoch' \
                        from med_fecha+med_hora) / 300 )) * 300)\
                        AT TIME ZONE 'UTC' as interval_alias\
                        FROM medicion_medicion\
                        where est_id_id=%s and var_id_id=%s and \
                        med_fecha>=%s and med_fecha<=%s\
                        GROUP BY interval_alias\
                        order by interval_alias",[estacion,variable,fecha_inicio,fecha_fin])
            else:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT avg(med_valor) as valor, \
                        avg(med_maximo)as maximo,avg(med_minimo) as minimo,\
                        to_timestamp(floor((extract('epoch' \
                        from med_fecha+med_hora) / 300 )) * 300)\
                        AT TIME ZONE 'UTC' as interval_alias\
                        FROM medicion_medicion\
                        where est_id_id=%s and var_id_id=%s and \
                        med_fecha>=%s and med_fecha<=%s\
                        GROUP BY interval_alias\
                        order by interval_alias",[estacion,variable,fecha_inicio,fecha_fin])
            datos=self.dictfetchall(cursor)
        #frecuencia horaria
        elif(frecuencia==str(2)):
            consulta=consulta.annotate(year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha'),
                hour=ExtractHour('med_hora')
            ).values('year','month','day','hour')
            if(variable==str(1)):
                datos=list(consulta.annotate(valor=Sum('med_valor')).
                values('valor','year','month','day','hour').
                order_by('year','month','day','hour'))
            else:
                datos=list(consulta.annotate(valor=Avg('med_valor'),
                maximo=Max('med_maximo'),minimo=Min('med_minimo')).
                values('valor','maximo','minimo','year','month','day','hour').
                order_by('year','month','day','hour'))

        #frecuencia diaria
        elif(frecuencia==str(3)):
            consulta=consulta.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha')
            ).values('year','month','day')
            if(variable==str(1)):
                datos=list(consulta.annotate(valor=Sum('med_valor')).
                values('valor','year','month','day').
                order_by('year','month','day'))
            else:
                datos=list(consulta.annotate(valor=Avg('med_valor'),
                maximo=Max('med_maximo'),minimo=Min('med_minimo')).
                values('valor','maximo','minimo','year','month','day').
                order_by('year','month','day'))

        #frecuencia mensual
        else:
            consulta=consulta.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha')
            ).values('month','year')
            if(variable==str(1)):
                consulta=list(consulta.annotate(valor=Sum('med_valor')).
                values('valor','month','year').
                order_by('year','month'))
            else:
                consulta=list(consulta.annotate(valor=Avg('med_valor'),
                maximo=Max('med_maximo'),minimo=Min('med_minimo')).
                values('valor','maximo','minimo','month','year').
                order_by('year','month'))

        return datos
    def dictfetchall(self,cursor):
        #Return all rows from a cursor as a dict
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
