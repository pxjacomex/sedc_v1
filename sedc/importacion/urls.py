from django.conf.urls import url
from importacion import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns=[
    url(r'^importacion/$',views.ImportacionList.as_view(),name='importacion_index'),
    #url(r'importacion/create/$', views.ImportacionCreate.as_view(), name='importacion_create'),
    url(r'importacion/detail/(?P<pk>[0-9]+)/$', views.ImportacionDetail.as_view(), name='importacion_detail'),
    url(r'importacion/importar/$', views.importar_archivo, name='importar'),
    url(r'importacion/guardar/$', views.guardar_archivo, name='guardar'),
    url(r'^ajax/formatos',views.lista_formatos,name='formatos')
]
