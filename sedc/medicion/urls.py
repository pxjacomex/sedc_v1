from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'^medicion/$',views.MedicionList.as_view(),name='medicion_index'),
    url(r'medicion/create/$', views.MedicionCreate.as_view(), name='medicion_create'),
    url(r'medicion/detail/(?P<pk>[0-9]+)/$', views.MedicionDetail.as_view(), name='medicion_detail'),
    url(r'medicion/(?P<pk>[0-9]+)/$', views.MedicionUpdate.as_view(), name='medicion_update'),
    url(r'medicion/(?P<pk>[0-9]+)/delete/$', views.MedicionDelete.as_view(), name='medicion_delete'),

    url(r'^validacion/$',views.ValidacionList.as_view(),name='validacion_index'),
    url(r'validacion/create/$', views.ValidacionCreate.as_view(), name='validacion_create'),
    url(r'validacion/detail/(?P<pk>[0-9]+)/$', views.ValidacionDetail.as_view(), name='validacion_detail'),
    url(r'validacion/(?P<pk>[0-9]+)/$', views.ValidacionUpdate.as_view(), name='validacion_update'),
    url(r'validacion/(?P<pk>[0-9]+)/delete/$', views.ValidacionDelete.as_view(), name='validacion_delete'),

]
