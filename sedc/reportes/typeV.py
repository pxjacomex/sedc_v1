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
    def __init__(self,mes,N_vel,N_p,NE_vel,NE_p,E_vel,E_p,SE_vel,SE_p,S_vel,S_p,SO_vel,SO_p,O_vel,O_p,NO_vel,NO_p,calma,obs,vel_mayor,vel_mayor_dir,vel_media):
        self.mes = mes
        self.N_vel = N_vel
        self.N_p = N_p
        self.NE_vel = NE_vel
        self.NE_p = NE_p
        self.E_vel = E_vel
        self.E_p = E_p
        self.SE_vel = SE_vel
        self.SE_p = SE_p
        self.S_vel = S_vel
        self.S_p = S_p
        self.SO_vel = SO_vel
        self.SO_p = SO_p
        self.O_vel = O_vel
        self.O_p = O_p
        self.NO_vel = NO_vel
        self.NO_p = NO_p
        self.calma = calma #listo
        self.obs = obs #listo
        self.vel_mayor = vel_mayor #listo
        self.vel_mayor_dir = vel_mayor_dir
        self.vel_media = vel_media

class TypeV(Titulos):
    '''consulta y crea la matriz de datos y el grafico para variable: 3'''
    def consulta(self,estacion,periodo):
        #annotate agrupa los valores en base a un campo y a una operacion
        #consulta=Medicion.objects.filter(est_id=estacion).filter(var_id=variable).filter(med_fecha__year=periodo).annotate(month=TruncMonth('med_fecha')).values('month')
        datos_calma=list(Medicion.objects
            .filter(est_id=estacion)
            .filter(var_id=4)
            .filter(med_fecha__year=periodo)
            .filter(med_valor__lt=0.5)
            .annotate(month=ExtractMonth('med_fecha'))
            .values('month').order_by('month'))

        datos_obs=list(Medicion.objects
            .filter(est_id=estacion)
            .filter(var_id=4)
            .filter(med_fecha__year=periodo)
            .exclude(med_valor__isnull=True)
            .annotate(month=ExtractMonth('med_fecha'))
            .values('month').order_by('month'))

        calma,obs = self.calmaobs(datos_calma ,datos_obs)

        consulta=Medicion.objects.filter(est_id=estacion).filter(var_id=4).filter(med_fecha__year=periodo).annotate(month=TruncMonth('med_fecha')).values('month')
        vel_mayor=list(consulta.annotate(c=Max('med_maximo')).values('c').order_by('month'))
        vel_media=list(consulta.annotate(c=Avg('med_valor')).values('c').order_by('month'))
        vel_mayor_simple = [d.get('c') for d in vel_mayor]
        vel_media_simple = [d.get('c') for d in vel_media]
        vel_media_kmh = [x * int(3.6) for x in vel_media_simple]

        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        #return max_simple,maxdia_simple,min_simple,mindia_simple,avg_simple,meses
        return calma,obs,vel_mayor_simple,vel_media_kmh
    def matriz(self,estacion, variable, periodo):
        max_simple,maxdia_simple,min_simple,mindia_simple,avg_simple,meses=self.consulta(estacion, variable, periodo)
        matrix = []
        for i in range(len(max_simple)):
            matrix.append(Resumen(meses[i],max_simple[i],maxdia_simple[i],min_simple[i],mindia_simple[i],avg_simple[i]))
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

    """def maximostai(self, datos_diarios_max):
        max_abs = []
        maxdia = []
        for i in range(1,13):
            val_max_abs=[]
            val_maxdia = []
            for fila in datos_diarios_max:
                if fila.get('month') == i:
                    val_max_abs.append(fila.get('valor'))
                    val_maxdia.append(fila.get('day'))
            max_abs.append(max(val_max_abs))
            maxdia.append(val_maxdia[val_max_abs.index(max(val_max_abs))])
        return max_abs,maxdia

    def minimostai(self, datos_diarios_min):
        min_abs = []
        mindia = []
        for i in range(1,13):
            val_min_abs=[]
            val_mindia = []
            for fila in datos_diarios_min:
                if fila.get('month') == i:
                    val_min_abs.append(fila.get('valor'))
                    val_mindia.append(fila.get('day'))
            min_abs.append(min(val_min_abs))
            mindia.append(val_mindia[val_min_abs.index(min(val_min_abs))])
        return min_abs,mindia"""


    def calmaobs(self,datos_calma,datos_obs):
        calma = []
        obs = []
        for i in range(1,13):
            count_calma = 0
            count_obs = 0
            for fila in datos_calma:
                if fila.get('month') == i:
                    count_calma += 1
            calma.append(count_calma)
            for fila in datos_obs:
                if fila.get('month') == i:
                    count_obs += 1
            obs.append(count_obs)
        calma_p = [(float(calmai)/obsi)*100 for calmai,obsi in zip(calma,obs)]
        return calma_p, obs
