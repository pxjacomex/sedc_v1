from django.conf.urls import url
from registro import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'logmedicion/$',views.LogMedicionList.as_view(),name='logmedicion_index'),
    url(r'logmedicion/(?P<page>[0-9]+)/$',views.LogMedicionList.as_view(),name='logmedicion_index'),
    url(r'logmedicion/detail/(?P<pk>[0-9]+)/$', views.LogMedicionDetail.as_view(), name='logmedicion_detail'),

]
