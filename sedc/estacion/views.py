# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Estacion, Registro, Vacios
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

# Create your views here.
class EstacionCreate(CreateView):
    model = Estacion
    fields = ['est_id', 'est_codigo','est_nombre','est_tipo','est_provincia','est_latitud','est_longitud','est_altura','est_ficha']
    def form_valid(self, form):
        return super(EstacionCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EstacionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
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

class EstacionList(ListView):
    model=Estacion
    paginate_by = 10
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EstacionList, self).get_context_data(**kwargs)
    	lista=Estacion.objects.all()
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
        return context

class EstacionDetail(DetailView):
    model=Estacion
class EstacionUpdate(UpdateView):
    model=Estacion
    fields = ['est_id', 'est_codigo','est_nombre','est_tipo','est_provincia','est_latitud','est_longitud','est_altura','est_ficha']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EstacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class EstacionDelete(DeleteView):
    model=Estacion
    success_url = reverse_lazy('estacion:estacion_index')

#Registro
class RegistroCreate(CreateView):
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

class RegistroList(ListView):
    model=Registro
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(RegistroList, self).get_context_data(**kwargs)
    	lista=Registro.objects.all()
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
        return context

class RegistroDetail(DetailView):
    model=Registro

class RegistroUpdate(UpdateView):
    model=Registro
    fields = ['est_id','reg_fecha','reg_archivo','reg_ubicacion']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RegistroUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class RegistroDelete(DeleteView):
    model=Registro
    success_url = reverse_lazy('estacion:registro_index')

#Vacios
class VaciosCreate(CreateView):
    model=Vacios
    fields = ['est_id','vac_fecha_ini','vac_fecha_fin','vac_observacion']
    def form_valid(self, form):
        return super(VaciosCreate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VaciosCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

class VaciosList(ListView):
    model=Vacios
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(VaciosList, self).get_context_data(**kwargs)
    	lista=Vacios.objects.all()
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
        return context

class VaciosDetail(DetailView):
    model=Vacios

class VaciosUpdate(UpdateView):
    model=Vacios
    fields = ['est_id','vac_fecha_ini','vac_fecha_fin','vac_observacion']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VaciosUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context

class VaciosDelete(DeleteView):
    model=Vacios
    success_url = reverse_lazy('estacion:vacios_index')
