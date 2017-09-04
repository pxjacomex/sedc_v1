from django.conf.urls import url
from validacion import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'^validacion/$',views.ValidacionList.as_view(),name='validacion_index'),
    url(r'validacion/create/$', views.ValidacionCreate.as_view(), name='validacion_create'),
    url(r'validacion/detail/(?P<pk>[0-9]+)/$', views.ValidacionDetail.as_view(), name='validacion_detail'),
    url(r'validacion/edit/(?P<pk>[0-9]+)/$', views.ValidacionUpdate.as_view(), name='validacion_update'),
    url(r'validacion/(?P<pk>[0-9]+)/delete/$', views.ValidacionDelete.as_view(), name='validacion_delete'),
    url(r'validacion/procesar/$', views.procesar_validacion, name='procesar_validacion'),
]
