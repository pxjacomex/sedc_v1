from django.conf.urls import url
from .views import HomePageView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^home/$', HomePageView.as_view(), name='home'),
]
