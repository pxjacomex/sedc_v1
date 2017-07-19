from django.conf.urls import url
from .views import ReportesPageView, ReportesAnuario
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    #url(r'^reportes/$', ReportesPageView.as_view(), name='reportes'),
    url(r'^reportes/anuario/$', ReportesAnuario.as_view(), name='anuario'),

]
