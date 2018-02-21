# -*- coding: utf-8 -*-
from formato.models import Formato,Asociacion
from importacion.functions import (consultar_formatos,guardar_datos,
    procesar_archivo_automatico,guardar_vacios)
from importacion.forms import UploadFileForm
def iniciar_lectura():
    formatos=list(Formato.objects.filter(for_tipo='automatico'))
    print len(formatos)
    for formato in formatos:
        #est_id=list(Asociacion.objects.annotate(est_id=ExtractYear('med_fecha')).values('year').distinct('year'))
        consulta=list(Asociacion.objects.filter(for_id=formato.for_id))
        estacion=consulta[0].est_id
        archivo=open(formato.for_ubicacion+formato.for_archivo)
        datos,variable=procesar_archivo_automatico(archivo,formato,estacion,formato.mar_id)
        for fila in datos:
            print fila
