# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Medicion
from django.views.generic import ListView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from medicion.forms import MedicionSearchForm
from django.db import connection

#Medicion views
class MedicionCreate(CreateView):
    model=Medicion
    fields = ['var_id','est_id','med_fecha','med_hora','med_valor','med_maximo',
              'med_minimo','med_validado']
    def form_valid(self, form):
        return super(MedicionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

"""class MedicionList(ListView):
    model=Medicion
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(MedicionList, self).get_context_data(**kwargs)
    	lista=Medicion.objects.all()
        page=self.request.GET.get('page')
    	paginator = Paginator(lista, 10)
    	if page is None:
    	    page=1
    	else:
    	    page=int(self.request.GET.get('page'))
    	if page == 1:
    	    start=1
            last=start+1
    	elif page == paginator.num_pages:
            last=paginator.num_pages
            start=last-1
        else:
    	    start=page-1
            last=page+1
        context['first'] = 1
        context['last'] = paginator.num_pages
        context['range'] = range(start,last+1)
        return context"""
class MedicionList(FormView):
    template_name='medicion/medicion_list.html'
    form_class=MedicionSearchForm
    success_url='/medicion/'
    lista=[]
    variable=""
    def post(self, request, *args, **kwargs):
        form=MedicionSearchForm(self.request.POST or None)
        if form.is_valid():
            self.lista=form.filtrar(form)
            self.variable=form.datos_variable(form)
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(MedicionList, self).get_context_data(**kwargs)
        context['lista']=self.lista
        context['variable']=self.variable
        return context
class MedicionFilter(FormView):
    template_name='medicion/medicion_filter.html'
    form_class=MedicionSearchForm
    success_url='/medicion/'

class MedicionDetail(DetailView):
    model=Medicion

class MedicionUpdate(UpdateView):
    model=Medicion
    fields = ['med_valor','med_maximo','med_minimo']
    url=""
    def get(self, request, *args, **kwargs):
        #print kwargs.get('pk')
        med_id=kwargs.get('pk')
        med_fecha=kwargs.get('fecha')
        med_hora=kwargs.get('hora')
        obj_medicion=Medicion.objects.filter(med_fecha=med_fecha)\
        .filter(med_hora=med_hora).get(med_id=med_id)
        self.object=obj_medicion
        self.url="/medicion/"+med_id+"/"+med_fecha+"/"+med_hora+"/"
        return self.render_to_response(self.get_context_data(**kwargs))
    def post(self, request, *args, **kwargs):
        med_id=kwargs.get('pk')
        med_fecha=kwargs.get('fecha')
        med_hora=kwargs.get('hora')
        obj_medicion=Medicion.objects.filter(med_fecha=med_fecha)\
        .filter(med_hora=med_hora).get(med_id=med_id)
        data=request.POST
        with connection.cursor() as cursor:
            cursor.execute("UPDATE medicion_medicion SET med_valor = %s, \
            med_maximo=%s, med_minimo=%s  WHERE med_fecha = %s \
            and med_hora=%s and med_id=%s",[data.get('med_valor'),
            data.get('med_maximo'),data.get('med_minimo'),med_fecha,med_hora,
            med_id])
        self.object=obj_medicion
        return self.render_to_response(self.get_context_data(**kwargs))
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        context['url']=self.url
        return context

class MedicionDelete(UpdateView):
    model=Medicion
    fields = ['est_id','var_id','med_fecha','med_valor','med_valor','med_maximo','med_minimo']
    url=""
    template_name='medicion/medicion_delete.html'
    def get(self, request, *args, **kwargs):
        med_id=kwargs.get('pk')
        med_fecha=kwargs.get('fecha')
        med_hora=kwargs.get('hora')
        obj_medicion=Medicion.objects.filter(med_fecha=med_fecha)\
        .filter(med_hora=med_hora).get(med_id=med_id)
        self.object=obj_medicion
        self.url="/medicion/delete/"+med_id+"/"+med_fecha+"/"+med_hora+"/"
        return self.render_to_response(self.get_context_data(**kwargs))
    def post(self, request, *args, **kwargs):
        med_id=kwargs.get('pk')
        med_fecha=kwargs.get('fecha')
        med_hora=kwargs.get('hora')
        obj_medicion=Medicion.objects.filter(med_fecha=med_fecha)\
        .filter(med_hora=med_hora).get(med_id=med_id)
        data=request.POST
        with connection.cursor() as cursor:
            cursor.execute("UPDATE medicion_medicion SET med_estado = false \
            WHERE med_fecha = %s \
            and med_hora=%s and med_id=%s",[med_fecha,med_hora,med_id])

        self.object=obj_medicion
        return self.render_to_response(self.get_context_data(**kwargs))
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionDelete, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        context['url']=self.url
        return context

def pagination(lista,page,num_reg):
    #lista=model.objects.all()
    paginator = Paginator(lista, num_reg)
    if page is None:
        page=1
    else:
        page=int(page)
    if page == 1:
        start=1
        last=start+1
    elif page == paginator.num_pages:
        last=paginator.num_pages
        start=last-1
    else:
        start=page-1
        last=page+1
    context={
        'first':'1',
        'last':paginator.num_pages,
        'range':range(start,last+1),
    }
    return context
