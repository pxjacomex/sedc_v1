from django.conf.urls import url
from marca import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'marca/$',views.MarcaList.as_view(),name='marca_index'),
    url(r'marca/(?P<page>[0-9]+)/$',views.MarcaList.as_view(),name='marca_index'),
    url(r'marca/create/$', views.MarcaCreate.as_view(), name='marca_create'),
    url(r'marca/detail/(?P<pk>[0-9]+)/$', views.MarcaDetail.as_view(), name='marca_detail'),
    url(r'marca/(?P<pk>[0-9]+)/$', views.MarcaUpdate.as_view(), name='marca_update'),
    url(r'marca/(?P<pk>[0-9]+)/delete/$', views.MarcaDelete.as_view(), name='marca_delete'),

]
