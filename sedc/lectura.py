# -*- coding: utf-8 -*-
import daemon
import time
from formato.models import Formato, Clasificacion
def iniciar_lectura():
    while True:
        with open("/tmp/current_time.txt", "w") as f:
            f.write("The time is now " + time.ctime())
        time.sleep(5)

def run():
    with daemon.DaemonContext():
        iniciar_lectura()

if __name__ == "__main__":
    run()
