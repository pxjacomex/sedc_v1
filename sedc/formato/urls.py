from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'formato/$',views.FormatoList.as_view(),name='formato_index'),
    url(r'formato/(?P<page>[0-9]+)/$',views.FormatoList.as_view(),name='formato_index'),
    url(r'formato/detail/(?P<pk>[0-9]+)/$', views.FormatoDetail.as_view(), name='formato_detail'),
    url(r'formato/(?P<pk>[0-9]+)/$', views.FormatoUpdate.as_view(), name='formato_update'),
    url(r'formato/(?P<pk>[0-9]+)/delete/$', views.FormatoDelete.as_view(), name='formato_delete'),

    url(r'^extension/$',views.ExtensionList.as_view(),name='extension_index'),
    url(r'extension/create/$', views.ExtensionCreate.as_view(), name='extension_create'),
    url(r'extension/detail/(?P<pk>[0-9]+)/$', views.ExtensionDetail.as_view(), name='extension_detail'),
    url(r'extension/(?P<pk>[0-9]+)/$', views.ExtensionUpdate.as_view(), name='extension_update'),
    url(r'extension/(?P<pk>[0-9]+)/delete/$', views.ExtensionDelete.as_view(), name='extension_delete'),

    url(r'^delimitador/$',views.DelimitadorList.as_view(),name='delimitador_index'),
    url(r'delimitador/create/$', views.DelimitadorCreate.as_view(), name='delimitador_create'),
    url(r'delimitador/detail/(?P<pk>[0-9]+)/$', views.DelimitadorDetail.as_view(), name='delimitador_detail'),
    url(r'delimitador/(?P<pk>[0-9]+)/$', views.DelimitadorUpdate.as_view(), name='delimitador_update'),
    url(r'delimitador/(?P<pk>[0-9]+)/delete/$', views.DelimitadorDelete.as_view(), name='delimitador_delete'),

    url(r'clasificacion/$',views.ClasificacionList.as_view(),name='clasificacion_index'),
    url(r'clasificacion/(?P<page>[0-9]+)/$',views.ClasificacionList.as_view(),name='clasificacion_index'),
    url(r'clasificacion/detail/(?P<pk>[0-9]+)/$', views.ClasificacionDetail.as_view(), name='clasificacion_detail'),
    url(r'clasificacion/(?P<pk>[0-9]+)/$', views.ClasificacionUpdate.as_view(), name='clasificacion_update'),
    url(r'clasificacion/(?P<pk>[0-9]+)/delete/$', views.ClasificacionDelete.as_view(), name='clasificacion_delete'),

    url(r'^asociacion/$',views.AsociacionList.as_view(),name='asociacion_index'),
    url(r'asociacion/create/$', views.AsociacionCreate.as_view(), name='asociacion_create'),
    url(r'asociacion/detail/(?P<pk>[0-9]+)/$', views.AsociacionDetail.as_view(), name='asociacion_detail'),
    url(r'asociacion/(?P<pk>[0-9]+)/$', views.AsociacionUpdate.as_view(), name='asociacion_update'),
    url(r'asociacion/(?P<pk>[0-9]+)/delete/$', views.AsociacionDelete.as_view(), name='asociacion_delete'),
]
