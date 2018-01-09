from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'frecuencia/$',views.FrecuenciaList.as_view(),name='frecuencia_index'),
    url(r'frecuencia/(?P<page>[0-9]+)/$',views.FrecuenciaList.as_view(),name='frecuencia_index'),
    url(r'frecuencia/create/$', views.FrecuenciaCreate.as_view(), name='frecuencia_create'),
    url(r'frecuencia/detail/(?P<pk>[0-9]+)/$', views.FrecuenciaDetail.as_view(), name='frecuencia_detail'),
    url(r'frecuencia/edit/(?P<pk>[0-9]+)/$', views.FrecuenciaUpdate.as_view(), name='frecuencia_update'),
    url(r'frecuencia/(?P<pk>[0-9]+)/delete/$', views.FrecuenciaDelete.as_view(), name='frecuencia_delete'),
]
