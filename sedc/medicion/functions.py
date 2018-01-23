# -*- coding: utf-8 -*-
from estacion.models import Estacion
from variable.models import Variable
from medicion.models import Medicion
from django.db.models import Max, Min, Avg, Count,Sum
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)
from datetime import datetime,timedelta,date
from django.db import connection

def filtrar(form):
    consulta=(Medicion.objects
    .filter(est_id=form.cleaned_data['estacion'])
    .filter(var_id=form.cleaned_data['variable'])
    .filter(med_fecha__range=[form.cleaned_data['inicio'],form.cleaned_data['fin']])
    )
    variable=Variable.objects.get(var_id=form.cleaned_data['variable'])
    #parametros para la resta consecutiva
    i=0
    ans=0
    datos=[]
    #parametros para la variabilidad
    valor_acumulado=0
    xi_acumulado=0
    hora0=datetime.strptime("00:00:00","%H:%M:%S")
    dat_var=[] #almacena las mediciones de una hora
    variabilidad=0
    for item in consulta:
        obj_analisis =Analisis()
        valor=item.med_valor
        valor_error=False
        resta=0
        resta_error=False
        var_error=False
        if valor<variable.var_minimo or valor>variable.var_maximo:
            valor_error=True
        #calculo de la resta consecutiva
        if i==0:
            resta=0
            ans=valor
            hora0=item.med_hora
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
        #variabilidad
        dif_minutos=int(item.med_hora.minute)-int(hora0.minute)
        dif_hora=int(item.med_hora.hour)-int(hora0.hour)
        valor_acumulado+=valor
        dat_var.append(item.med_valor)
        if (dif_minutos==58 and len(dat_var)==30) or (dif_minutos==59 and len(dat_var)==60) and dif_hora<1:
            promedio=sum(dat_var)/len(dat_var)
            for val in dat_var:
                xi_acumulado+=(val-promedio)**2
            variabilidad=float(xi_acumulado/len(dat_var)) ** 0.5
            dat_var=[]
            valor_acumulado=0
            xi_acumulado=0
        elif dif_hora>=1:
            hora0=item.med_hora
            variabilidad=0
        if variabilidad<variable.var_min:
            var_error=True

        #asignar al objeto analisis
        obj_analisis.iden=item.med_id
        obj_analisis.fecha=item.med_fecha
        obj_analisis.hora=item.med_hora
        obj_analisis.valor=item.med_valor
        obj_analisis.valor_error=valor_error
        obj_analisis.resta=abs(resta)
        obj_analisis.resta_error=resta_error
        obj_analisis.variabilidad=variabilidad
        obj_analisis.var_error=var_error
        datos.append(obj_analisis)

    return datos
def consultar(form):
    est_id=str(form.cleaned_data['estacion'])
    var_id=str(form.cleaned_data['variable'])
    fec_ini=str(form.cleaned_data['fec_ini'])+str(" ")+str(form.cleaned_data['hor_ini'])
    fec_fin=str(form.cleaned_data['fec_fin'])+str(" ")+str(form.cleaned_data['hor_fin'])
    consulta=list(Medicion.objects.raw(
        'SELECT med_id,med_fecha,med_hora,med_valor,med_maximo, med_minimo\
        FROM  medicion_medicion WHERE med_fecha+med_hora>=%s \
        and med_fecha+med_hora<=%s and est_id_id=%s\
        and var_id_id=%s',
        [fec_ini,fec_fin,est_id,var_id]
        )
    )

    return consulta
def eliminar(form):
    est_id=str(form.cleaned_data['estacion'])
    var_id=str(form.cleaned_data['variable'])
    fec_ini=str(form.cleaned_data['fec_ini'])+str(" ")+str(form.cleaned_data['hor_ini'])
    fec_fin=str(form.cleaned_data['fec_fin'])+str(" ")+str(form.cleaned_data['hor_fin'])
    print (str(form.cleaned_data['fec_ini'])+str(form.cleaned_data['hor_ini']))
    with connection.cursor() as cursor:
        cursor.execute("UPDATE medicion_medicion SET med_estado = false \
        WHERE est_id_id=%s\
        and var_id_id=%s and med_fecha+med_hora>=%s \
        and med_fecha+med_hora<=%s",
        [est_id,var_id,fec_ini,fec_fin] )
    return "Proceso Realizado"

def datos_variable(form):
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
    variabilidad=0
    var_error=False
