# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import HumedadAire
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear,ExtractMonth,ExtractDay,ExtractHour)
def matrizVI(estacion,variable,periodo):
    datos=[]
    obj_estacion=Estacion.objects.get(est_id=estacion)
