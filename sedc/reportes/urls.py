from django.conf.urls import url
from reportes import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^reportes/anuario/$', views.ReportesAnuario.as_view(), name='anuario'),
    url(r'^reportes/consultas/$',views.ConsultasPeriodo.as_view(),name='consultas_periodo'),
    url(r'^reportes/comparacion/$',views.ComparacionValores.as_view(),name='comparacion_reporte'),
]
