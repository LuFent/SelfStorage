from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout')
]
