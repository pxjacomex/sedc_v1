from django.views.generic.base import TemplateView
from .models import Medicion
from django.db.models import Max, Min, Avg
from django.db.models.functions import TruncMonth
from django.views.generic import FormView
from .forms import AnuarioForm

import plotly.offline as opy
import plotly.graph_objs as go

class Resumen(object):
    def __init__(self, mes, maximo, minimo, medio):
        self.mes = mes
        self.maximo= maximo
        self.minimo = minimo
        self.medio = medio


class ReportesAnuario(FormView):
    template_name='reportes/anuario_reporte.html'
    form_class=AnuarioForm
    success_url='/reportes/anuario/'
    lista={}
    def post(self, request, *args, **kwargs):
        form=AnuarioForm(self.request.POST or None)
        if form.is_valid():
            self.lista=form.filtrar(form)
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(ReportesAnuario, self).get_context_data(**kwargs)
        context.update(self.lista)
        return context
