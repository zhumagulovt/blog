from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import *


app_name = 'users'

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
]