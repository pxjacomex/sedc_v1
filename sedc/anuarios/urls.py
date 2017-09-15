from django.conf.urls import url
from anuarios import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    #url(r'^anuarios/$',views.ValidacionList.as_view(),name='validacion_index'),
    url(r'anuarios/procesar/$', views.ProcesarVariables.as_view(), name='anuarios_procesar'),

]
