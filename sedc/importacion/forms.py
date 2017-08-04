from django import forms
from estacion.models import Estacion
from medicion.models import Medicion
from variable.models import Variable
from validacion.models import Validacion
from datetime import datetime
from formato.models import Formato,Clasificacion,Delimitador

class UploadFileForm(forms.Form):
    def lista_estaciones():
        lista = ()
        estaciones = Estacion.objects.all()
        for item in estaciones:
            fila = ((str(item.est_id),item.est_codigo+str(" ")+item.est_nombre),)
            lista = lista + fila
        return lista
    def lista_formatos():
        lista = ()
        formatos = Formato.objects.all()
        for item in formatos:
            fila = ((str(item.for_id),item.for_descripcion+str(" ")),)
            lista = lista + fila
        return lista
    estacion=forms.ChoiceField(choices=lista_estaciones())
    formato=forms.ChoiceField(choices=lista_formatos())
    archivo = forms.FileField()
def procesar_archivo(archivo,form):
    formato=Formato.objects.get(for_id=form.cleaned_data['formato'])
    estacion=Estacion.objects.get(est_id=form.cleaned_data['estacion'])
    clasificacion=list(Clasificacion.objects.filter(
        for_id=formato.for_id).values())
    delimitador=Delimitador.objects.get(del_id=formato.del_id_id)
    i=0
    for linea in archivo.readlines():
        i+=1
        #controlar la fila de inicio
        if i>=formato.for_fil_ini:
            valores=linea.split(delimitador.del_caracter)
            if formato.for_col_hora==formato.for_col_hora:
                fecha_hora=datetime.strptime(valores[formato.for_col_hora], formato.for_fecha+str(" ")+formato.for_hora)
                fecha=fecha_hora.strftime('%Y-%m-%d')
                hora=fecha_hora.strftime('%H:%M:%S')
            for fila in clasificacion:
                variable=Variable.objects.get(var_id=fila['var_id_id'])
                if fila['cla_valor'] is not None:
                    valor=float(valores[fila['cla_valor']])
                else:
                    valor=None
                if fila['cla_maximo'] is not None:
                    maximo=float(valores[fila['cla_maximo']])
                else:
                    maximo=None
                if fila['cla_minimo'] is not None:
                    minimo=float(valores[fila['cla_minimo']])
                else:
                    minimo=None
                print estacion.est_id,variable,fecha,hora,valor,maximo,minimo
                med=Validacion(var_id=variable,est_id=estacion,
                    val_fecha=fecha,val_hora=hora,
                    val_valor=valor,val_maximo=maximo,val_minimo=minimo,
                    val_estado=True)
                med.save()
    Validacion.objects.all().delete()
