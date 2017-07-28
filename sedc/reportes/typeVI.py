# -*- coding: utf-8 -*-

from django import forms
from medicion.models import Medicion
from variable.models import Variable,Unidad
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
import plotly.offline as opy
import plotly.graph_objs as go
from reportes.titulos import Titulos
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)
import datetime

class Resumen(object):
    def __init__(self,mes,max_5,max_6,max_7,max_8,max_9,max_10,max_11,max_12,\
                 max_13,max_14,max_15,max_16,max_17,max_18,max_abs,max_hora,\
                 min_5,min_6,min_7,min_8,min_9,min_10,min_11,min_12,min_13,\
                 min_14,min_15,min_16,min_17,min_18,min_abs,min_hora):
        self.mes = mes
        self.max_5 = max_5
        self.max_6 = max_6
        self.max_7 = max_7
        self.max_8 = max_8
        self.max_9 = max_9
        self.max_10 = max_10
        self.max_11 = max_11
        self.max_12 = max_12
        self.max_13 = max_13
        self.max_14  = max_14
        self.max_15 = max_15
        self.max_16 = max_16
        self.max_17 = max_17
        self.max_18 = max_18
        self.max_abs = max_abs
        self.max_hora = max_hora

        self.mes = mes
        self.min_5 = min_5
        self.min_6 = min_6
        self.min_7 = min_7
        self.min_8 = min_8
        self.min_9 = min_9
        self.min_10 = min_10
        self.min_11 = min_11
        self.min_12 = min_12
        self.min_13 = min_13
        self.min_14  = min_14
        self.min_15 = min_15
        self.min_16 = min_16
        self.min_17 = min_17
        self.min_18 = min_18
        self.min_abs = min_abs
        self.min_hora = min_hora

class TypeVI(Titulos):
    '''consulta y crea la matriz de datos y el grafico para variable: 7'''
    def consulta(self,estacion,variable,periodo):
        #annotate agrupa los valores en base a un campo y a una operacion

        datos_diarios_max=list(Medicion.objects
            .filter(est_id=estacion)
            .filter(var_id=variable)
            .filter(med_fecha__year=periodo)
            .filter(med_hora__range=(datetime.datetime.strptime('05:00:00', '%H:%M:%S').time()\
                                     ,datetime.datetime.strptime('18:00:00', '%H:%M:%S').time()))
            .annotate(month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha'),hour=ExtractHour('med_hora'))
            .values('month','day','hour')
            .annotate(valor=Max('med_valor'))
            .values('valor','month','day','hour').order_by('month'))
        datos_diarios_min=list(Medicion.objects
            .filter(est_id=estacion)
            .filter(var_id=variable)
            .filter(med_fecha__year=periodo)
            .filter(med_hora__range=(datetime.datetime.strptime('05:00:00', '%H:%M:%S').time()\
                                     ,datetime.datetime.strptime('18:00:00', '%H:%M:%S').time()))
            .annotate(month=ExtractMonth('med_fecha'),day=ExtractDay('med_fecha'),hour=ExtractHour('med_hora'))
            .values('month','day','hour')
            .annotate(valor=Min('med_valor'))
            .values('valor','month','day','hour').order_by('month'))


        max_5,max_6,max_7,max_8,max_9,max_10,max_11,max_12,max_13,max_14,max_15,\
        max_16,max_17,max_18 = self.max_hora_rad(datos_diarios_max)
        min_5,min_6,min_7,min_8,min_9,min_10,min_11,min_12,min_13,min_14,min_15,\
        min_16,min_17,min_18 = self.min_hora_rad(datos_diarios_min)
        max_abs,max_hora = self.maximosrad(datos_diarios_max)
        min_abs,min_hora = self.minimosrad(datos_diarios_min)

        mes=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return mes,max_5,max_6,max_7,max_8,max_9,max_10,max_11,max_12,max_13,max_14,\
        max_15,max_16,max_17,max_18,max_abs,max_hora,min_5,min_6,min_7,min_8,min_9,\
        min_10,min_11,min_12,min_13,min_14,min_15,min_16,min_17,min_18,min_abs,min_hora

    def matriz(self,estacion, variable, periodo):
        mes,max_5,max_6,max_7,max_8,max_9,max_10,max_11,max_12,max_13,max_14,\
        max_15,max_16,max_17,max_18,max_abs,max_hora,min_5,min_6,min_7,\
        min_8,min_9,min_10,min_11,min_12,min_13,min_14,min_15,min_16,min_17,\
        min_18,min_abs,min_hora=self.consulta(estacion, variable, periodo)
        matrix = []
        for i in range(len(max_abs)):
            matrix.append(Resumen(mes[i],max_5[i],max_6[i],max_7[i],max_8[i],max_9[i],max_10[i],max_11[i],max_12[i]
                                  ,max_13[i],max_14[i],max_15[i],max_16[i],max_17[i],max_18[i],max_abs[i],max_hora[i]
                                  ,min_5[i],min_6[i],min_7[i],min_8[i],min_9[i],min_10[i],min_11[i],min_12[i]
                                  ,min_13[i],min_14[i],min_15[i],min_16[i],min_17[i],min_18[i],min_abs[i],min_hora[i]))
        return matrix

    def maximosrad(self, datos_diarios_max):
        max_abs = []
        max_hora = []
        for i in range(1,13):
            val_max_abs=[]
            val_max_hora = []
            for fila in datos_diarios_max:
                if fila.get('month') == i:
                    val_max_abs.append(fila.get('valor'))
                    val_max_hora.append(fila.get('hour'))
            max_abs.append(max(val_max_abs))
            max_hora.append(val_max_hora[val_max_abs.index(max(val_max_abs))])
        return max_abs,max_hora

    def minimosrad(self, datos_diarios_min):
        min_abs = []
        min_hora = []
        for i in range(1,13):
            val_min_abs=[]
            val_min_hora = []
            for fila in datos_diarios_min:
                if fila.get('month') == i:
                    val_min_abs.append(fila.get('valor'))
                    val_min_hora.append(fila.get('hour'))
            min_abs.append(min(val_min_abs))
            min_hora.append(val_min_hora[val_min_abs.index(min(val_min_abs))])
        return min_abs,min_hora

    def max_hora_rad(self, datos_diarios_max):
        max_5 = []
        max_6 = []
        max_7 = []
        max_8 = []
        max_9 = []
        max_10 = []
        max_11 = []
        max_12 = []
        max_13 = []
        max_14 = []
        max_15 = []
        max_16 = []
        max_17 = []
        max_18 = []
        for i in range (1,13):
            val_max_5 = []
            val_max_6 = []
            val_max_7 = []
            val_max_8 = []
            val_max_9 = []
            val_max_10 = []
            val_max_11 = []
            val_max_12 = []
            val_max_13 = []
            val_max_14 = []
            val_max_15 = []
            val_max_16 = []
            val_max_17 = []
            val_max_18 = []
            for fila in datos_diarios_max:
                if fila.get('month') == i:
                    if fila.get('hour') == 5:
                        val_max_5.append(fila.get('valor'))
                    elif fila.get('hour') == 6:
                        val_max_6.append(fila.get('valor'))
                    elif fila.get('hour') == 7:
                        val_max_7.append(fila.get('valor'))
                    elif fila.get('hour') == 8:
                        val_max_8.append(fila.get('valor'))
                    elif fila.get('hour') == 9:
                        val_max_9.append(fila.get('valor'))
                    elif fila.get('hour') == 10:
                        val_max_10.append(fila.get('valor'))
                    elif fila.get('hour') == 11:
                        val_max_11.append(fila.get('valor'))
                    elif fila.get('hour') == 12:
                        val_max_12.append(fila.get('valor'))
                    elif fila.get('hour') == 13:
                        val_max_13.append(fila.get('valor'))
                    elif fila.get('hour') == 14:
                        val_max_14.append(fila.get('valor'))
                    elif fila.get('hour') == 15:
                        val_max_15.append(fila.get('valor'))
                    elif fila.get('hour') == 16:
                        val_max_16.append(fila.get('valor'))
                    elif fila.get('hour') == 17:
                        val_max_17.append(fila.get('valor'))
                    elif fila.get('hour') == 18:
                        val_max_18.append(fila.get('valor'))
            max_5.append(max(val_max_5))
            max_6.append(max(val_max_6))
            max_7.append(max(val_max_7))
            max_8.append(max(val_max_8))
            max_9.append(max(val_max_9))
            max_10.append(max(val_max_10))
            max_11.append(max(val_max_11))
            max_12.append(max(val_max_12))
            max_13.append(max(val_max_13))
            max_14.append(max(val_max_14))
            max_15.append(max(val_max_15))
            max_16.append(max(val_max_16))
            max_17.append(max(val_max_17))
            max_18.append(max(val_max_18))
        return max_5,max_6,max_7,max_8,max_9,max_10,max_11,max_12,max_13,max_14,\
        max_15,max_16,max_17,max_18

    def min_hora_rad(self, datos_diarios_min):
        min_5 = []
        min_6 = []
        min_7 = []
        min_8 = []
        min_9 = []
        min_10 = []
        min_11 = []
        min_12 = []
        min_13 = []
        min_14 = []
        min_15 = []
        min_16 = []
        min_17 = []
        min_18 = []
        for i in range (1,13):
            val_min_5 = []
            val_min_6 = []
            val_min_7 = []
            val_min_8 = []
            val_min_9 = []
            val_min_10 = []
            val_min_11 = []
            val_min_12 = []
            val_min_13 = []
            val_min_14 = []
            val_min_15 = []
            val_min_16 = []
            val_min_17 = []
            val_min_18 = []
            for fila in datos_diarios_min:
                if fila.get('month') == i:
                    if fila.get('hour') == 5:
                        val_min_5.append(fila.get('valor'))
                    elif fila.get('hour') == 6:
                        val_min_6.append(fila.get('valor'))
                    elif fila.get('hour') == 7:
                        val_min_7.append(fila.get('valor'))
                    elif fila.get('hour') == 8:
                        val_min_8.append(fila.get('valor'))
                    elif fila.get('hour') == 9:
                        val_min_9.append(fila.get('valor'))
                    elif fila.get('hour') == 10:
                        val_min_10.append(fila.get('valor'))
                    elif fila.get('hour') == 11:
                        val_min_11.append(fila.get('valor'))
                    elif fila.get('hour') == 12:
                        val_min_12.append(fila.get('valor'))
                    elif fila.get('hour') == 13:
                        val_min_13.append(fila.get('valor'))
                    elif fila.get('hour') == 14:
                        val_min_14.append(fila.get('valor'))
                    elif fila.get('hour') == 15:
                        val_min_15.append(fila.get('valor'))
                    elif fila.get('hour') == 16:
                        val_min_16.append(fila.get('valor'))
                    elif fila.get('hour') == 17:
                        val_min_17.append(fila.get('valor'))
                    elif fila.get('hour') == 18:
                        val_min_18.append(fila.get('valor'))
            min_5.append(min(val_min_5))
            min_6.append(min(val_min_6))
            min_7.append(min(val_min_7))
            min_8.append(min(val_min_8))
            min_9.append(min(val_min_9))
            min_10.append(min(val_min_10))
            min_11.append(min(val_min_11))
            min_12.append(min(val_min_12))
            min_13.append(min(val_min_13))
            min_14.append(min(val_min_14))
            min_15.append(min(val_min_15))
            min_16.append(min(val_min_16))
            min_17.append(min(val_min_17))
            min_18.append(min(val_min_18))
        return min_5,min_6,min_7,min_8,min_9,min_10,min_11,min_12,min_13,min_14,\
        min_15,min_16,min_17,min_18
