from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'^variable/$',views.VariableList.as_view(),name='variable_index'),
    url(r'variable/create/$', views.VariableCreate.as_view(), name='variable_create'),
    url(r'variable/detail/(?P<pk>[0-9]+)/$', views.VariableDetail.as_view(), name='variable_detail'),
    url(r'variable/(?P<pk>[0-9]+)/$', views.VariableUpdate.as_view(), name='variable_update'),
    url(r'variable/(?P<pk>[0-9]+)/delete/$', views.VariableDelete.as_view(), name='variable_delete'),

    url(r'^unidad/$',views.UnidadList.as_view(),name='unidad_index'),
    url(r'unidad/create/$', views.UnidadCreate.as_view(), name='unidad_create'),
    url(r'unidad/detail/(?P<pk>[0-9]+)/$', views.UnidadDetail.as_view(), name='unidad_detail'),
    url(r'unidad/(?P<pk>[0-9]+)/$', views.UnidadUpdate.as_view(), name='unidad_update'),
    url(r'unidad/(?P<pk>[0-9]+)/delete/$', views.UnidadDelete.as_view(), name='unidad_delete'),

    url(r'control/$',views.ControlList.as_view(),name='control_index'),
    url(r'control/(?P<page>[0-9]+)/$',views.ControlList.as_view(),name='control_index'),
    url(r'control/create/$', views.ControlCreate.as_view(), name='control_create'),
    url(r'control/detail/(?P<pk>[0-9]+)/$', views.ControlDetail.as_view(), name='control_detail'),
    url(r'control/(?P<pk>[0-9]+)/$', views.ControlUpdate.as_view(), name='control_update'),
    url(r'control/(?P<pk>[0-9]+)/delete/$', views.ControlDelete.as_view(), name='control_delete'),

]
