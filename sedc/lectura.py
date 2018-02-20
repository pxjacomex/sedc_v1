# -*- coding: utf-8 -*-
import daemon
import time
from formato.models import Formato, Clasificacion
def iniciar_lectura():
    formatos=list(Formato.objects.filter(for_tipo='automático'))
    for fila in formatos:
        print fila.for_archivo
iniciar_lectura()
'''def run():
    with daemon.DaemonContext():
        iniciar_lectura()

if __name__ == "__main__":
    run()'''
