from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'^medicion/$',views.MedicionList.as_view(),name='medicion_index'),
    url(r'^medicion/listdelete/$',views.ListDelete.as_view(),name='list_delete'),
    url(r'^medicion/filter/$',views.MedicionFilter.as_view(),name='medicion_filter'),
    url(r'^medicion/filterdelete/$',views.FilterDelete.as_view(),name='filter_delete'),
    url(r'medicion/create/$', views.MedicionCreate.as_view(), name='medicion_create'),
    url(r'medicion/detail/(?P<pk>[0-9]+)/$', views.MedicionDetail.as_view(), name='medicion_detail'),
    url(r'medicion/(?P<pk>[0-9]+)/(?P<fecha>[0-9-]+)/(?P<var_id>[0-9]+)/$', views.MedicionUpdate.as_view(), name='medicion_update'),
    url(r'medicion/delete/(?P<pk>[0-9]+)/(?P<fecha>[0-9-]+)/(?P<var_id>[0-9]+)/$', views.MedicionDelete.as_view(), name='medicion_delete'),

]
