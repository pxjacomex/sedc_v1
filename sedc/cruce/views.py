# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from cruce.models import Cruce
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from cruce.forms import CruceSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
#Cruce views
class CruceCreate(LoginRequiredMixin,CreateView):
    model=Cruce
    fields = ['cru_id','est_id','var_id']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CruceCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class CruceList(LoginRequiredMixin,ListView,FormView):
    model=Cruce
    paginate_by = 10
    template_name='cruce/cruce_list.html'
    form_class=CruceSearchForm
    #parametros propios
    cadena=str("")
    def get(self, request, *args, **kwargs):
        form=CruceSearchForm(self.request.GET or None)
        self.object_list=Cruce.objects.all()
        if form.is_valid():
            self.object_list=form.filtrar(form)
            self.cadena=form.cadena(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CruceList, self).get_context_data(**kwargs)
        page=self.request.GET.get('page')
        print kwargs
        context.update(pagination(self.object_list,page,10))
        context["cadena"]=self.cadena
        return context

class CruceDetail(LoginRequiredMixin,DetailView):
    model=Cruce

class CruceUpdate(LoginRequiredMixin,UpdateView):
    model=Cruce
    fields = ['cru_id','est_id','var_id']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CruceUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class CruceDelete(LoginRequiredMixin,DeleteView):
    model=Cruce
    success_url = reverse_lazy('cruce:cruce_index')
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
