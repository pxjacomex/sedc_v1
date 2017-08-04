from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'vacios/$',views.VaciosList.as_view(),name='vacios_index'),
    url(r'vacios/(?P<page>[0-9]+)/$',views.VaciosList.as_view(),name='vacios_index'),
    url(r'vacios/create/$', views.VaciosCreate.as_view(), name='vacios_create'),
    url(r'vacios/detail/(?P<pk>[0-9]+)/$', views.VaciosDetail.as_view(), name='vacios_detail'),
    url(r'vacios/(?P<pk>[0-9]+)/$', views.VaciosUpdate.as_view(), name='vacios_update'),
    url(r'vacios/(?P<pk>[0-9]+)/delete/$', views.VaciosDelete.as_view(), name='vacios_delete'),
]
