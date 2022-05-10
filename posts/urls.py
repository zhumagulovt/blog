from django.urls import path

from .views import *


urlpatterns = [
    path('', PostAPIList.as_view()),
    path('<int:pk>/', PostAPIUpdate.as_view())
]