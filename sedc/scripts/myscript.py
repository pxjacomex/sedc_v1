# -*- coding: utf-8 -*-
from formato.models import Formato,Asociacion
from importacion.functions import (consultar_formatos,guardar_datos,
    procesar_archivo_automatico,guardar_vacios)
from importacion.forms import UploadFileForm
import daemon
import time
def iniciar_lectura():
    while True:
        formatos=list(Formato.objects.filter(for_tipo='automatico'))
        for formato in formatos:
            consulta=list(Asociacion.objects.filter(for_id=formato.for_id))
            estacion=consulta[0].est_id
            archivo=open(formato.for_ubicacion+formato.for_archivo)
            datos,variables=procesar_archivo_automatico(archivo,formato,estacion,formato.mar_id)
def run():
    with daemon.DaemonContext():
        iniciar_lectura()
