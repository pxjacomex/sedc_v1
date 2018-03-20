# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Vacios
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import VaciosSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
#Vacios
class VaciosCreate(LoginRequiredMixin,CreateView):
    model=Vacios
    fields = ['est_id','var_id','vac_fecha_ini','vac_hora_ini','vac_fecha_fin','vac_hora_fin','vac_observacion']
    def form_valid(self, form):
        return super(VaciosCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VaciosCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class VaciosList(LoginRequiredMixin,ListView,FormView):
    #parámetros ListView
    model=Vacios
    paginate_by=10
    #parámetros FormView
    template_name='vacios/vacios_list.html'
    form_class=VaciosSearchForm
    #parametros propios
    def post(self, request, *args, **kwargs):
        form=VaciosSearchForm(self.request.POST or None)
        page=kwargs.get('page')
        if form.is_valid() and self.request.is_ajax():
            self.object_list=form.filtrar(form)
        else:
            self.object_list=Vacios.objects.all()
        context = super(VaciosList, self).get_context_data(**kwargs)
        context.update(pagination(self.object_list,page,10))
        #return self.render_to_response(self.get_context_data(form=form))
        return render(request,'vacios/vacios_table.html',context)
    def get_context_data(self, **kwargs):
        context = super(VaciosList, self).get_context_data(**kwargs)
        page=self.request.GET.get('page')
        context.update(pagination(self.object_list,page,10))
        return context

class VaciosDetail(LoginRequiredMixin,DetailView):
    model=Vacios

class VaciosUpdate(LoginRequiredMixin,UpdateView):
    model=Vacios
    fields = ['est_id','var_id','vac_fecha_ini','vac_hora_ini','vac_fecha_fin','vac_hora_fin','vac_observacion']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VaciosUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class VaciosDelete(LoginRequiredMixin,DeleteView):
    model=Vacios
    success_url = reverse_lazy('vacios:vacios_index')

def pagination(lista,page,num_reg):
    #lista=model.objects.all()
    paginator = Paginator(lista, num_reg)
    print paginator.num_pages
    factor=paginator.num_pages//2
    if factor>5:
        factor=5
    print factor
    if page is None:
        page=1
    else:
        page=int(page)
    if page == 1:
        start=1
        last=factor
    elif page == paginator.num_pages:
        last=paginator.num_pages
        start=last-1
    elif (page-factor)<0:
        start=1
        last=factor
    elif page>(paginator.num_pages-factor):
        start=page-factor
        last=paginator.num_pages
    else:
        start=page-factor//2
        last=page+factor//2
    context={
        'first':'1',
        'last':paginator.num_pages,
        'range':range(start,last+1),
    }
    return context
