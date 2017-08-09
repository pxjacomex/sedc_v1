from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'datalogger/$',views.DataloggerList.as_view(),name='datalogger_index'),
    url(r'datalogger/(?P<page>[0-9]+)/$',views.DataloggerList.as_view(),name='datalogger_index'),
    url(r'datalogger/create/$', views.DataloggerCreate.as_view(), name='datalogger_create'),
    url(r'datalogger/detail/(?P<pk>[0-9]+)/$', views.DataloggerDetail.as_view(), name='datalogger_detail'),
    url(r'datalogger/edit/(?P<pk>[0-9]+)/$', views.DataloggerUpdate.as_view(), name='datalogger_update'),
    url(r'datalogger/(?P<pk>[0-9]+)/delete/$', views.DataloggerDelete.as_view(), name='datalogger_delete'),

    url(r'sensor/$',views.SensorList.as_view(),name='sensor_index'),
    url(r'sensor/(?P<page>[0-9]+)/$',views.SensorList.as_view(),name='sensor_index'),
    url(r'sensor/create/$', views.SensorCreate.as_view(), name='sensor_create'),
    url(r'sensor/detail/(?P<pk>[0-9]+)/$', views.SensorDetail.as_view(), name='sensor_detail'),
    url(r'sensor/edit/(?P<pk>[0-9]+)/$', views.SensorUpdate.as_view(), name='sensor_update'),
    url(r'sensor/(?P<pk>[0-9]+)/delete/$', views.SensorDelete.as_view(), name='sensor_delete'),
]
