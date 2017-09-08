# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from validacion.models import Validacion
from django.views.generic import ListView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from validacion.forms import ValidacionProcess
from validacion import functions
# Create your views here.

class ValidacionCreate(CreateView):
    model=Validacion
    fields = ['est_id','var_id','val_fecha','val_num_dat','val_fre_reg','val_porcentaje']
    def get_context_data(self, **kwargs):
        context = super(ValidacionCreate, self).get_context_data(**kwargs)
        context['title'] = "Crear"
        return context

class ValidacionList(ListView):
    model=Validacion
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(ValidacionList, self).get_context_data(**kwargs)
    	lista=Validacion.objects.all()
        page=self.request.GET.get('page')
    	context.update(pagination(self.object_list,page,10))
        return context

class ValidacionDetail(DetailView):
    model=Validacion

class ValidacionUpdate(UpdateView):
    model=Validacion
    fields = ['est_id','var_id','val_fecha','val_num_dat','val_fre_reg','val_porcentaje']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ValidacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class ValidacionDelete(DeleteView):
    model=Validacion
    success_url = reverse_lazy('medicion:validacion_index')
def procesar_validacion(request):
    if request.method=='POST':
        form=ValidacionProcess(request.POST)
        #if form.is_valid():

    else:
        form=ValidacionProcess()
    return render(request,'validacion/validacion_procesar.html',{'form':form})
#lista de validaciones por estacion y fechas
def lista_validacion(request):
    if request.method=='POST':
        form=ValidacionProcess(request.POST or None)
        estacion=request.POST['estacion']
        
        datos=functions.generar_validacion(estacion)
    else:
        datos=[]
    return render(request,'validacion/validacion_filtro.html',{'datos':datos})

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
