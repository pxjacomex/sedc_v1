from django.conf.urls import url

from cruce import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'cruce/$',views.CruceList.as_view(),name='cruce_index'),
    url(r'cruce/(?P<page>[0-9]+)/$',views.CruceList.as_view(),name='cruce_index'),
    url(r'cruce/create/$', views.CruceCreate.as_view(), name='cruce_create'),
    url(r'cruce/detail/(?P<pk>[0-9]+)/$', views.CruceDetail.as_view(), name='cruce_detail'),
    url(r'cruce/edit/(?P<pk>[0-9]+)/$', views.CruceUpdate.as_view(), name='cruce_update'),
    url(r'cruce/(?P<pk>[0-9]+)/delete/$', views.CruceDelete.as_view(), name='cruce_delete'),

]
