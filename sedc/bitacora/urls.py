from django.conf.urls import url
from bitacora import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'bitacora/$',views.BitacoraList.as_view(),name='bitacora_index'),
    url(r'bitacora/(?P<page>[0-9]+)/$',views.BitacoraList.as_view(),name='bitacora_index'),
    url(r'bitacora/create/$', views.BitacoraCreate.as_view(), name='bitacora_create'),
    url(r'bitacora/detail/(?P<pk>[0-9]+)/$', views.BitacoraDetail.as_view(), name='bitacora_detail'),
    url(r'bitacora/edit/(?P<pk>[0-9]+)/$', views.BitacoraUpdate.as_view(), name='bitacora_update'),
    url(r'bitacora/(?P<pk>[0-9]+)/delete/$', views.BitacoraDelete.as_view(), name='bitacora_delete'),

]
