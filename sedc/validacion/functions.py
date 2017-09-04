# -*- coding: utf-8 -*-
from validacion.models import Validacion
from frecuencia.models import Frecuencia
from medicion.models import Medicion
from datetime import datetime,timedelta
def generar_validacion(form):
    estacion=form.cleaned_data['estacion']
    inicio=datetime.strptime(form.cleaned_data['inicio'],'%d/%m/%Y')
    fin=datetime.strptime(form.cleaned_data['inicio'],'%d/%m/%Y')
    variables=Frecuencia.objects.filter(est_id=estacion).distinct('var_id')
    for variable in variables:
        consulta=Validacion.objects.filter(est_id=estacion)\
            .filter(var_id=variable).order_by('-val_fecha')[:0]
        if consulta.exists():
            fecha_ini=datetime.strptime(consulta.get('fre_valor'),'%d/%m/%Y')
        else:
            frecuencia=Frecuencia.objects.filter(est_id=estacion)\
            .filter(var_id=variable).order_by('fre_fecha_ini')[:0]
            fecha_ini=datetime.strptime(frecuencia.get('fre_valor'),'%d/%m/%Y')




            #obj_val=Validacion(est_id=estacion,)
