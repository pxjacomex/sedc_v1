from django.conf.urls import url
from instalacion import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'instalacion/$',views.InstalacionList.as_view(),name='instalacion_index'),
    url(r'instalacion/(?P<page>[0-9]+)/$',views.InstalacionList.as_view(),name='instalacion_index'),
    url(r'instalacion/create/$', views.InstalacionCreate.as_view(), name='instalacion_create'),
    url(r'instalacion/detail/(?P<pk>[0-9]+)/$', views.InstalacionDetail.as_view(), name='instalacion_detail'),
    url(r'instalacion/edit/(?P<pk>[0-9]+)/$', views.InstalacionUpdate.as_view(), name='instalacion_update'),
    url(r'instalacion/(?P<pk>[0-9]+)/delete/$', views.InstalacionDelete.as_view(), name='instalacion_delete'),


]
