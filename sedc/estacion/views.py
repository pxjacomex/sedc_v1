# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Estacion#, Registro
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import EstacionSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class EstacionCreate(LoginRequiredMixin,CreateView):
    model = Estacion
    fields = ['est_id', 'est_codigo','est_nombre','est_tipo','est_provincia','est_estado','est_latitud','est_longitud','est_altura','est_ficha']
    def form_valid(self, form):
        return super(EstacionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EstacionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        print "context"
        return context
    def model_form_upload(request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = DocumentForm()
        return render(request, 'core/model_form_upload.html', {
            'form': form
        })

class EstacionList(LoginRequiredMixin,ListView,FormView):
    #parámetros ListView
    model=Estacion
    paginate_by=10
    #parámetros FormView
    template_name='estacion/estacion_list.html'
    form_class=EstacionSearchForm
    #parametros propios
    cadena=str("")
    def get(self, request, *args, **kwargs):
        form=EstacionSearchForm(self.request.GET or None)
        self.object_list=Estacion.objects.all()

        if form.is_valid():
            self.object_list=form.filtrar(form)
            self.cadena=form.cadena(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(EstacionList, self).get_context_data(**kwargs)
        page=self.request.GET.get('page')
        print page
        context.update(pagination(self.object_list,page,10))
        context["cadena"]=self.cadena
        return context

class EstacionDetail(LoginRequiredMixin,DetailView):
    model=Estacion
class EstacionUpdate(LoginRequiredMixin,UpdateView):
    model=Estacion
    fields = ['est_id', 'est_codigo','est_nombre','est_tipo','est_provincia','est_estado','est_latitud','est_longitud','est_altura','est_ficha']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EstacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class EstacionDelete(LoginRequiredMixin,DeleteView):
    model=Estacion
    success_url = reverse_lazy('estacion:estacion_index')

#Registro
'''
class RegistroCreate(LoginRequiredMixin,CreateView):
    model=Registro
    fields = ['est_id','reg_fecha','reg_archivo','reg_ubicacion']
    def form_valid(self, form):
        return super(RegistroCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RegistroCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class RegistroList(LoginRequiredMixin,ListView):
    model=Registro
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(RegistroList, self).get_context_data(**kwargs)
    	lista=Registro.objects.all()
        page=self.request.GET.get('page')
        context.update(pagination(self.object_list,page,10))
        return context

class RegistroDetail(LoginRequiredMixin,DetailView):
    model=Registro

class RegistroUpdate(LoginRequiredMixin,UpdateView):
    model=Registro
    fields = ['est_id','reg_fecha','reg_archivo','reg_ubicacion']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RegistroUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class RegistroDelete(LoginRequiredMixin,DeleteView):
    model=Registro
    success_url = reverse_lazy('estacion:registro_index')'''

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
