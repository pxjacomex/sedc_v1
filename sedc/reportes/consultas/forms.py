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
        ('0','Instantaneo'),
        ('1','Horario'),
        ('2','Diario'),
        ('3','Mensual'),
    )
    estacion=forms.ChoiceField(choices=lista_estaciones())
    variable=forms.ChoiceField(choices=lista_variables())
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

        #frecuencia instantanea
        if(form.cleaned_data['frecuencia']==str(0)):
            consulta=consulta.values('med_valor','med_fecha','med_hora').\
            order_by('med_fecha','med_hora')

        #frecuencia horaria
        elif(form.cleaned_data['frecuencia']==str(1)):
            consulta=consulta.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha'),
                hour=ExtractHour('med_hora')
            ).values('year','month','day','hour')
            if(form.cleaned_data['variable']==str(1)):
                consulta=consulta.annotate(valor=Sum('med_valor')).\
                values('valor','year','month','day','hour').\
                order_by('year','month','day','hour')
            else:
                consulta=consulta.annotate(valor=Avg('med_valor')).\
                values('valor','year','month','day','hour').\
                order_by('year','month','day','hour')

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
                order_by('year','month','day')
            else:
                consulta=consulta.annotate(valor=Avg('med_valor')).\
                values('valor','year','month','day').\
                order_by('year','month','day')

        #frecuencia mensual
        else:
            consulta=consulta.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha')
            ).values('month','year')
            if(form.cleaned_data['variable']==str(1)):
                consulta=consulta.annotate(valor=Sum('med_valor')).\
                values('valor','month','year').\
                order_by('year','month')
            else:
                consulta=consulta.annotate(valor=Avg('med_valor')).\
                values('valor','month','year').\
                order_by('year','month')

        return consulta

    def filtrar_temp(self,form):
        #filtrar los datos por estacion, variable y rango de fechas
        #SOLO PARA TEMPERATURA
        consulta=(Medicion.objects
        .filter(est_id=form.cleaned_data['estacion'])
        .filter(var_id=form.cleaned_data['variable'])
        .filter(med_fecha__range=[form.cleaned_data['inicio'],
            form.cleaned_data['fin']]))

        #frecuencia instantanea
        if(form.cleaned_data['frecuencia']==str(0)):
            consulta_avg=consulta.values('med_valor','med_fecha','med_hora').\
            order_by('med_fecha','med_hora')
            consulta_max=consulta.values('med_maximo','med_fecha','med_hora').\
            order_by('med_fecha','med_hora')
            consulta_min=consulta.values('med_minimo','med_fecha','med_hora').\
            order_by('med_fecha','med_hora')

        #frecuencia horaria
        elif(form.cleaned_data['frecuencia']==str(1)):
            consulta=consulta.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha'),
                hour=ExtractHour('med_hora')
            ).values('year','month','day','hour')

            consulta_avg=consulta.annotate(valor=Avg('med_valor')).\
            values('valor','year','month','day','hour').\
            order_by('year','month','day','hour')

            consulta_max=consulta.annotate(valor=Max('med_maximo')).\
            values('valor','year','month','day','hour').\
            order_by('year','month','day','hour')

            consulta_min=consulta.annotate(valor=Min('med_minimo')).\
            values('valor','year','month','day','hour').\
            order_by('year','month','day','hour')

        #frecuencia diaria
        elif(form.cleaned_data['frecuencia']==str(2)):
            consulta=consulta.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha'),
                day=ExtractDay('med_fecha')
            ).values('year','month','day')

            consulta_avg=consulta.annotate(valor=Avg('med_valor')).\
            values('valor','year','month','day').\
            order_by('year','month','day')

            consulta_max=consulta.annotate(valor=Max('med_maximo')).\
            values('valor','year','month','day').\
            order_by('year','month','day')

            consulta_min=consulta.annotate(valor=Min('med_minimo')).\
            values('valor','year','month','day').\
            order_by('year','month','day')

        #frecuencia mensual
        else:
            consulta=consulta.annotate(
                year=ExtractYear('med_fecha'),
                month=ExtractMonth('med_fecha')
            ).values('month','year')

            consulta_avg=consulta.annotate(valor=Avg('med_valor')).\
            values('valor','year','month').\
            order_by('year','month')

            consulta_max=consulta.annotate(valor=Max('med_maximo')).\
            values('valor','year','month').\
            order_by('year','month')

            consulta_min=consulta.annotate(valor=Min('med_minimo')).\
            values('valor','year','month').\
            order_by('year','month')

        return consulta_avg,consulta_max,consulta_min

    def data_simple(self,form):
        consulta = self.filtrar(form)

        #frecuencia instantanea
        if(form.cleaned_data['frecuencia']==str(0)):
            val = [d.get('med_valor') for d in consulta]
            freq = []
            for fila in list(consulta):
                freq.append(datetime.datetime.combine(fila['med_fecha'],fila['med_hora']))

        #frecuencia horaria
        elif(form.cleaned_data['frecuencia']==str(1)):
            val = [d.get('valor') for d in consulta]
            hour = [d.get('hour') for d in consulta]
            day = [d.get('day') for d in consulta]
            month = [d.get('month') for d in consulta]
            year = [d.get('year') for d in consulta]
            freq = []
            for i in range(len(list(consulta))):
                fecha_str = str(year[i])+":"+str(month[i])+":"+str(day[i])
                fecha = datetime.datetime.strptime(fecha_str,'%Y:%m:%d').date()
                freq.append(datetime.datetime.combine(fecha,datetime.time(hour[i])))

        #frecuencia diaria
        elif(form.cleaned_data['frecuencia']==str(2)):
            val = [d.get('valor') for d in consulta]
            day = [d.get('day') for d in consulta]
            month = [d.get('month') for d in consulta]
            year = [d.get('year') for d in consulta]
            freq = []
            for i in range(len(list(consulta))):
                fecha_str = str(year[i])+":"+str(month[i])+":"+str(day[i])
                fecha = datetime.datetime.strptime(fecha_str,'%Y:%m:%d').date()
                freq.append(fecha)

        #frecuencia mensual
        else:
            val = [d.get('valor') for d in consulta]
            month = [d.get('month') for d in consulta]
            year = [d.get('year') for d in consulta]
            freq = []
            for i in range(len(list(consulta))):
                fecha_str = str(calendar.month_abbr[month[i]])+" "+str(year[i])
                freq.append(fecha_str)

        return val,freq

    def data_simple_temp(self,form):
        #SOLO PARA TEMPERATURA
        consulta_avg,consulta_max,consulta_min = self.filtrar_temp(form)

        #frecuencia instantanea
        if(form.cleaned_data['frecuencia']==str(0)):
            val_avg = [d.get('med_valor') for d in consulta_avg]
            val_max = [d.get('med_maximo') for d in consulta_max]
            val_min = [d.get('med_minimo') for d in consulta_min]
            freq = []
            for fila in list(consulta_avg):
                freq.append(datetime.datetime.combine(fila['med_fecha'],fila['med_hora']))

        #frecuencia horaria
        elif(form.cleaned_data['frecuencia']==str(1)):
            val_avg = [d.get('valor') for d in consulta_avg]
            val_max = [d.get('valor') for d in consulta_max]
            val_min = [d.get('valor') for d in consulta_min]
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
            val_avg = [d.get('valor') for d in consulta_avg]
            val_max = [d.get('valor') for d in consulta_max]
            val_min = [d.get('valor') for d in consulta_min]
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
            val_avg = [d.get('valor') for d in consulta_avg]
            val_max = [d.get('valor') for d in consulta_max]
            val_min = [d.get('valor') for d in consulta_min]
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
                mode = 'lines',
                line = dict(
                    color = ('rgb(205, 12, 24)'),
                    )
            )
            trace1 = go.Scatter(
                x = freq,
                y = val_min,
                name = 'Min',
                mode = 'lines',
                line = dict(
                    color = ('rgb(50, 205, 50)'),
                    )
            )
            trace2 = go.Scatter(
                x = freq,
                y = val_avg,
                name = 'Media',
                mode = 'lines',
                line = dict(
                    color = ('rgb(22, 96, 167)'),
                    )
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
        consulta=list(Estacion.objects.filter(est_id=estacion))
        return consulta[0]

    def titulo_variable(self,variable):
        consulta=list(Variable.objects.filter(var_id=variable))
        return consulta[0]

    def titulo_unidad(self,variable):
        var=list(Variable.objects.filter(var_id=variable).values())
        uni=list(Unidad.objects.filter(uni_id=var[0].get('uni_id_id')).values())
        return (uni[0].get('uni_sigla')).encode('utf-8')

    def titulo_frecuencia(self,frecuencia):
        nombre = []
        if frecuencia == '0':
            nombre = 'Instantanea'
        elif frecuencia == '1':
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
