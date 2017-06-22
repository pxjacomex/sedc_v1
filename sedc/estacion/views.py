# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import (render,
    get_object_or_404,
    redirect)
from .models import Estacion

# Create your views here.
def home(request):
    estacion=Estacion.objects.order_by('est_id')
    template=loader.get_template('index.html')
    context={
        'estacion':estacion
    }
    return HttpResponse(template.render(context,request))
