# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Max, Min
from medicion.models import Medicion

# Create your models here.
year = str(2012)

if med_fecha in range(year + '-01-01',year + '-01-31'):
    med_valor__max = Medicion.objects.all().aggregate(Max('med_valor'))
    med_valor__min = Medicion.objects.all().aggregate(Min('med_valor'))
    med_valor__med = Medicion.objects.all().aggregate(Median('med_valor'))
elif med_fecha in range(year + '-02-01',year + '-02-29'):
    med_valor__max = Medicion.objects.all().aggregate(Max('med_valor'))
    med_valor__min = Medicion.objects.all().aggregate(Min('med_valor'))
    med_valor__med = Medicion.objects.all().aggregate(Median('med_valor'))
