# -*- coding: utf-8 -*-

from django import forms
from medicion.models import Medicion
from variable.models import Variable,Unidad
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count, Case, When
import plotly.offline as opy
import plotly.graph_objs as go
from reportes.titulos import Titulos
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)

class Resumen(object):
    #def __init__(self,mes,N_vel,N_p,NE_vel,NE_p,E_vel,E_p,SE_vel,SE_p,S_vel,S_p,SO_vel,SO_p,O_vel,O_p,NO_vel,NO_p,calma,obs,vel_mayor,vel_mayor_dir,vel_media):
    def __init__(self,mes,vvi,calma,obs):
        self.mes = mes
        self.N_vel = vvi[0]
        self.N_p = vvi[1]
        self.NE_vel = vvi[2]
        self.NE_p = vvi[3]
        self.E_vel = vvi[4]
        self.E_p = vvi[5]
        self.SE_vel = vvi[6]
        self.SE_p = vvi[7]
        self.S_vel = vvi[8]
        self.S_p = vvi[9]
        self.SO_vel = vvi[10]
        self.SO_p = vvi[11]
        self.O_vel = vvi[12]
        self.O_p = vvi[13]
        self.NO_vel = vvi[14]
        self.NO_p = vvi[15]

        self.calma = calma #listo
        self.obs = obs #listo
        """self.vel_mayor = vel_mayor #listo
        self.vel_mayor_dir = vel_mayor_dir
        self.vel_media = vel_media #listo"""
class Viento(object):
    def __init__(self,dvi,vvi):
        self.dvi=dvi
        self.vvi=vvi
#clase para agrupar la velocidad y direccion del viento.
class TypeV(Titulos):
    '''consulta y crea la matriz de datos y el grafico para variable: 3'''
    def consulta(self,estacion,periodo):

        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        #return max_simple,maxdia_simple,min_simple,mindia_simple,avg_simple,meses
        return calma,num_obs,meses

    def matriz(self,estacion, variable, periodo):
        meses,vvi,calma,obs=self.observaciones(estacion, periodo)
        matrix = []
        for i in range(len(meses)):
            matrix.append(Resumen(meses[i],vvi[i],calma[i],obs[i]))
        return matrix

    def grafico(self,estacion, variable, periodo):
        max_simple,maxdia_simple,min_simple,mindia_simple,avg_simple,meses=self.consulta(estacion, variable, periodo)
        trace0 = go.Scatter(
            x = meses,
            y = max_simple,
            name = 'Max',
            line = dict(
                color = ('rgb(22, 96, 167)'),
                width = 4)
        )
        trace1 = go.Scatter(
            x = meses,
            y = min_simple,
            name = 'Min',
            line = dict(
                color = ('rgb(205, 12, 24)'),
                width = 4,)
        )
        trace2 = go.Scatter(
            x = meses,
            y = avg_simple,
            name = 'Media',
            line = dict(
                color = ('rgb(50, 205, 50)'),
                width = 4,)
        )
        data = go.Data([trace0, trace1, trace2])
        layout = go.Layout(title = str(self.titulo_grafico(variable)) + str(" (") + str(self.titulo_unidad(variable)) + str(")"))
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
        return div



    def observaciones(self,estacion,periodo):
        obs=[]
        calma=[]
        vvi=[]
        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        for i in range(1,13):
            datos_obs=(Medicion.objects
                .filter(est_id=estacion).filter(var_id=4)
                .filter(med_fecha__year=periodo)
                .filter(med_fecha__month=i)
                .exclude(med_valor__isnull=True).count())
            datos_calma=(Medicion.objects
                .filter(est_id=estacion).filter(var_id=4)
                .filter(med_fecha__year=periodo)
                .filter(med_fecha__month=i)
                .filter(med_valor__lt=0.5).count())
            obs.append(datos_obs)
            calma.append((float(datos_calma)/datos_obs)*100)
            vvi.append(self.viento(estacion,periodo,i,datos_obs))
        return meses,vvi,calma,obs
    def viento(self,estacion,periodo,mes,datos_obs):
        vvi=[[0 for x in range(0)] for y in range(8)]
        dat_dvi=list(Medicion.objects
            .filter(est_id=estacion).filter(var_id=5)
            .filter(med_fecha__year=periodo).filter(med_fecha__month=mes)
            .values('med_valor').order_by('med_fecha','med_hora')
        )
        dat_vvi=list(Medicion.objects
            .filter(est_id=estacion).filter(var_id=4)
            .filter(med_fecha__year=periodo).filter(med_fecha__month=mes)
            .values('med_valor').order_by('med_fecha','med_hora')
        )
        for val_dvi,val_vvi in zip(dat_dvi,dat_vvi):
            item=Viento(val_dvi.get('med_valor'),val_vvi.get('med_valor'))
            if val_vvi.get('med_valor') is not None:
                if val_dvi.get('med_valor') < 22.5 or val_dvi.get('med_valor')>337.5:
                    vvi[0].append(val_vvi.get('med_valor'))
                elif val_dvi.get('med_valor') < 67.5:
                    vvi[1].append(val_vvi.get('med_valor'))
                elif val_dvi.get('med_valor') < 112.5:
                    vvi[2].append(val_vvi.get('med_valor'))
                elif val_dvi.get('med_valor') < 157.5:
                    vvi[3].append(val_vvi.get('med_valor'))
                elif val_dvi.get('med_valor') < 202.5:
                    vvi[4].append(val_vvi.get('med_valor'))
                elif val_dvi.get('med_valor') < 247.5:
                    vvi[5].append(val_vvi.get('med_valor'))
                elif val_dvi.get('med_valor') < 292.5:
                    vvi[6].append(val_vvi.get('med_valor'))
                elif val_dvi.get('med_valor') < 337.5:
                    vvi[7].append(val_vvi.get('med_valor'))
        valores=[]
        for j in range(8):
            valores.append(float(sum(vvi[j])/len(vvi[j])))
            valores.append(float(len(vvi[j]))/datos_obs*100)
        return valores
