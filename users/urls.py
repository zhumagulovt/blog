from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *


app_name = 'users'

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('search/', SearchUserView.as_view(), name='user-search'),
    path('<str:slug>/', ProfileDetailView.as_view(), name='profile-detail'),
]