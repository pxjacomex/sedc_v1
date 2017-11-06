from django.conf.urls import url
from sensor import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[

    url(r'sensor/$',views.SensorList.as_view(),name='sensor_index'),
    url(r'sensor/(?P<page>[0-9]+)/$',views.SensorList.as_view(),name='sensor_index'),
    url(r'sensor/create/$', views.SensorCreate.as_view(), name='sensor_create'),
    url(r'sensor/detail/(?P<pk>[0-9]+)/$', views.SensorDetail.as_view(), name='sensor_detail'),
    url(r'sensor/edit/(?P<pk>[0-9]+)/$', views.SensorUpdate.as_view(), name='sensor_update'),
    url(r'sensor/(?P<pk>[0-9]+)/delete/$', views.SensorDelete.as_view(), name='sensor_delete'),
]
