from django.conf.urls import url
from django.urls import reverse_lazy
from home.views import HomePageView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import(
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    #url(r'^$', LoginView.as_view(), name='login'),
    url(r'^login/$', LoginView.as_view(template_name='home/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout')
]
