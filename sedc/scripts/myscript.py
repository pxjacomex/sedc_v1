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
            if len(consulta)>0:
                estacion=consulta[0].est_id
                archivo=open(formato.for_ubicacion+formato.for_archivo)
                datos,variables=procesar_archivo_automatico(archivo,formato,estacion,formato.mar_id)
                if len(datos)>0:
                    print time.ctime()
                    guardar_datos_automatico(datos,variables)
                    print time.ctime()
                    registro=open('/tmp/sedc.txt','a')
                    registro.write(time.ctime()+': Información guardada '+str(estacion.est_codigo)+str(formato.for_descripcion)+'\n')
                    registro.close()

                else:
                    registro=open('/tmp/sedc.txt','a')
                    registro.write(time.ctime()+': No existe nueva informacion'+'\n')
                    registro.close()
            else:
                registro=open('/tmp/sedc.txt','a')
                registro.write(time.ctime()+': No existen formatos para iniciar la lectura'+'\n')
                registro.close()
                break
def run(*args):
    with daemon.DaemonContext():
        iniciar_lectura()
