from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'estacion/$',views.EstacionList.as_view(),name='estacion_index'),
    url(r'estacion/(?P<page>[0-9]+)/$',views.EstacionList.as_view(),name='estacion_index'),
    url(r'estacion/create/$', views.EstacionCreate.as_view(), name='estacion_create'),
    url(r'estacion/detail/(?P<pk>[0-9]+)/$', views.EstacionDetail.as_view(), name='estacion_detail'),
    url(r'estacion/edit/(?P<pk>[0-9]+)/$', views.EstacionUpdate.as_view(), name='estacion_update'),
    url(r'estacion/(?P<pk>[0-9]+)/delete/$', views.EstacionDelete.as_view(), name='estacion_delete'),

]
