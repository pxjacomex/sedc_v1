# -*- coding: utf-8 -*-
from formato.models import Formato,Asociacion
from importacion.functions import (consultar_formatos,guardar_datos,
    procesar_archivo,guardar_vacios)
from importacion.forms import UploadFileForm
def iniciar_lectura():
    formatos=list(Formato.objects.filter(for_tipo='automático'))
    #for fila in formatos:
        #Asociacion.objects.
