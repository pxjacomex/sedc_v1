from django.conf.urls import url
from .views import ReportesAnuario,ConsultasPeriodo
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^reportes/anuario/$', ReportesAnuario.as_view(), name='anuario'),
    url(r'^reportes/consultas/$',ConsultasPeriodo.as_view(),name='consultas_periodo'),
]
