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
        variables=Variable.objects.all()
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

    #consulta_avg para agrupar los datos por hora, diario y mes
    def filtrar(self,form):
        #filtrar los datos por estacion, variable y rango de fechas
        consulta_avg=(Medicion.objects
        .filter(est_id=form.cleaned_data['estacion'])
        .filter(var_id=form.cleaned_data['variable'])
        .filter(med_fecha__range=[form.cleaned_data['inicio'],
            form.cleaned_data['fin']]))
        #frecuencia horaria
        if(form.cleaned_data['frecuencia']==str(1)):
            consulta_avg=consulta_avg.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha'),
                hour=ExtractHour('med_hora')
            ).values('year','month','day','hour')
            if(form.cleaned_data['variable']==str(1)):
                consulta_avg=consulta_avg.annotate(valor=Sum('med_valor')).\
                values('valor','year','month','day','hour').\
                order_by('month','day','year','hour')
            else:
                consulta_avg=consulta_avg.annotate(valor=Avg('med_valor')).\
                values('valor','year','month','day','hour').\
                order_by('month','day','year','hour')

        #frecuencia diaria
        elif(form.cleaned_data['frecuencia']==str(2)):
            consulta_avg=consulta_avg.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha')
            ).values('year','month','day')
            if(form.cleaned_data['variable']==str(1)):
                consulta_avg=consulta_avg.annotate(valor=Sum('med_valor')).\
                values('valor','year','month','day').\
                order_by('month','day','year')
            else:
                consulta_avg=consulta_avg.annotate(valor=Avg('med_valor')).\
                values('valor','year','month','day').\
                order_by('month','day','year')

        #frecuencia mensual
        else:
            consulta_avg=consulta_avg.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha')
            ).values('month','year')
            if(form.cleaned_data['variable']==str(1)):
                consulta_avg=consulta_avg.annotate(valor=Sum('med_valor')).\
                values('valor','month','year').\
                order_by('month')
            else:
                consulta_avg=consulta_avg.annotate(valor=Avg('med_valor')).\
                values('valor','month','year').\
                order_by('month')

        return consulta_avg

    def filtrar_temp(self,form):
        #filtrar los datos por estacion, variable y rango de fechas
        #SOLO PARA TEMPERATURA
        consulta_avg=(Medicion.objects
        .filter(est_id=form.cleaned_data['estacion'])
        .filter(var_id=form.cleaned_data['variable'])
        .filter(med_fecha__range=[form.cleaned_data['inicio'],
            form.cleaned_data['fin']]))
        #frecuencia horaria
        if(form.cleaned_data['frecuencia']==str(1)):
            consulta_avg=consulta_avg.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha'),
                hour=ExtractHour('med_hora')
            ).values('year','month','day','hour')

            consulta_avg_avg=consulta_avg.annotate(valor=Avg('med_valor')).\
            values('valor','year','month','day','hour').\
            order_by('month','day','year','hour')

            consulta_avg_max=consulta_avg.annotate(valor=Avg('med_maximo')).\
            values('valor','year','month','day','hour').\
            order_by('month','day','year','hour')

            consulta_avg_min=consulta_avg.annotate(valor=Avg('med_minimo')).\
            values('valor','year','month','day','hour').\
            order_by('month','day','year','hour')

        #frecuencia diaria
        elif(form.cleaned_data['frecuencia']==str(2)):
            consulta_avg=consulta_avg.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha')
            ).values('year','month','day')

            consulta_avg_avg=consulta_avg.annotate(valor=Avg('med_valor')).\
            values('valor','year','month','day').\
            order_by('month','day','year')

            consulta_avg_max=consulta_avg.annotate(valor=Avg('med_maximo')).\
            values('valor','year','month','day').\
            order_by('month','day','year')

            consulta_avg_min=consulta_avg.annotate(valor=Avg('med_minimo')).\
            values('valor','year','month','day').\
            order_by('month','day','year')

        #frecuencia mensual
        else:
            consulta_avg=consulta_avg.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha')
            ).values('month','year')

            consulta_avg_avg=consulta_avg.annotate(valor=Avg('med_valor')).\
            values('valor','year','month').\
            order_by('month')

            consulta_avg_max=consulta_avg.annotate(valor=Max('med_maximo')).\
            values('valor','year','month').\
            order_by('month')

            consulta_avg_min=consulta_avg.annotate(valor=Min('med_minimo')).\
            values('valor','year','month').\
            order_by('month')

        return consulta_avg_avg,consulta_avg_max,consulta_avg_min

    def data_simple(self,form):
        consulta_avg = self.filtrar(form)

        val = [d.get('valor') for d in consulta_avg]
        #frecuencia horaria
        if(form.cleaned_data['frecuencia']==str(1)):
            hour = [d.get('hour') for d in consulta_avg]
            day = [d.get('day') for d in consulta_avg]
            month = [d.get('month') for d in consulta_avg]
            year = [d.get('year') for d in consulta_avg]
            freq = []
            for i in range(len(list(consulta_avg))):
                fecha_str = str(year[i])+":"+str(month[i])+":"+str(day[i])
                fecha = datetime.datetime.strptime(fecha_str,'%Y:%m:%d').date()
                freq.append(datetime.datetime.combine(fecha,datetime.time(hour[i])))

        #frecuencia diaria
        elif(form.cleaned_data['frecuencia']==str(2)):
            day = [d.get('day') for d in consulta_avg]
            month = [d.get('month') for d in consulta_avg]
            year = [d.get('year') for d in consulta_avg]
            freq = []
            for i in range(len(list(consulta_avg))):
                fecha_str = str(year[i])+":"+str(month[i])+":"+str(day[i])
                fecha = datetime.datetime.strptime(fecha_str,'%Y:%m:%d').date()
                freq.append(fecha)

        #frecuencia mensual
        else:
            month = [d.get('month') for d in consulta_avg]
            year = [d.get('year') for d in consulta_avg]
            freq = []
            for i in range(len(list(consulta_avg))):
                fecha_str = str(calendar.month_abbr[month[i]])+" "+str(year[i])
                freq.append(fecha_str)

        return val,freq

    def data_simple_temp(self,form):
        #SOLO PARA TEMPERATURA
        consulta_avg,consulta_max,consulta_min = self.filtrar_temp(form)

        val_avg = [d.get('valor') for d in consulta_avg]
        val_max = [d.get('valor') for d in consulta_max]
        val_min = [d.get('valor') for d in consulta_min]

        if(form.cleaned_data['frecuencia']==str(1)):
            hour = [d.get('hour') for d in consulta_avg]
            day = [d.get('day') for d in consulta_avg]
            month = [d.get('month') for d in consulta_avg]
            year = [d.get('year') for d in consulta_avg]
            freq = []
            for i in range(len(list(consulta_avg))):
                fecha_str = str(year[i])+":"+str(month[i])+":"+str(day[i])
                fecha = datetime.datetime.strptime(fecha_str,'%Y:%m:%d').date()
                freq.append(datetime.datetime.combine(fecha,datetime.time(hour[i])))

        #frecuencia diaria
        elif(form.cleaned_data['frecuencia']==str(2)):
            day = [d.get('day') for d in consulta_avg]
            month = [d.get('month') for d in consulta_avg]
            year = [d.get('year') for d in consulta_avg]
            freq = []
            for i in range(len(list(consulta_avg))):
                fecha_str = str(year[i])+":"+str(month[i])+":"+str(day[i])
                fecha = datetime.datetime.strptime(fecha_str,'%Y:%m:%d').date()
                freq.append(fecha)

        #frecuencia mensual
        else:
            month = [d.get('month') for d in consulta_avg]
            year = [d.get('year') for d in consulta_avg]
            freq = []
            for i in range(len(list(consulta_avg))):
                fecha_str = str(calendar.month_abbr[month[i]])+" "+str(year[i])
                freq.append(fecha_str)

        return val_avg,val_max,val_min,freq

    def grafico(self,form):
        if form.cleaned_data['variable']==str(2):
            val_avg,val_max,val_min,freq = self.data_simple_temp(form)

            trace0 = go.Scatter(
                x = freq,
                y = val_max,
                name = 'Max',
                line = dict(
                    color = ('rgb(22, 96, 167)'),
                    width = 4)
            )
            trace1 = go.Scatter(
                x = freq,
                y = val_min,
                name = 'Min',
                line = dict(
                    color = ('rgb(205, 12, 24)'),
                    width = 4,)
            )
            trace2 = go.Scatter(
                x = freq,
                y = val_avg,
                name = 'Media',
                line = dict(
                    color = ('rgb(50, 205, 50)'),
                    width = 4,)
            )
            data = go.Data([trace0, trace1, trace2])

        else:
            val,freq = self.data_simple(form)

            trace = go.Scatter(
                x = freq,
                y = val,
                name = str(form.cleaned_data['variable']),
                mode = 'lines',
            )
            data = go.Data([trace])

        layout = go.Layout(
            title = str(self.titulo_variable(form.cleaned_data['variable'])) +\
            " " + str(self.titulo_frecuencia(form.cleaned_data['frecuencia']))+\
            " " + str(self.titulo_estacion(form.cleaned_data['estacion'])),
            yaxis = dict(title = str(self.titulo_variable(form.cleaned_data['variable'])) + \
                         str(" (") + str(self.titulo_unidad(form.cleaned_data['variable'])) + str(")"))
            )
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
        return div

    def titulo_estacion(self,estacion):
        consulta_avg=list(Estacion.objects.filter(est_id=estacion))
        return consulta_avg[0]

    def titulo_variable(self,variable):
        consulta_avg=list(Variable.objects.filter(var_id=variable))
        return consulta_avg[0]

    def titulo_unidad(self,variable):
        var=list(Variable.objects.filter(var_id=variable).values())
        uni=list(Unidad.objects.filter(uni_id=var[0].get('uni_id_id')).values())
        return (uni[0].get('uni_sigla')).encode('utf-8')

    def titulo_frecuencia(self,frecuencia):
        nombre = []
        if frecuencia == '1':
            nombre = 'Horaria'
        elif frecuencia == '2':
            nombre = 'Diaria'
        elif frecuencia == '3':
            nombre = 'Mensual'
        return nombre

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
