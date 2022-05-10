from django.urls import path

from .views import *


app_name = 'postapp'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('cats/', CategoryListView.as_view(), name='category-list'),
    path('search/', SearchResultView.as_view(), name='post-search'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('cat/<int:pk>/', CategoryDetailView.as_view(), name='category-detail')
    # path('create/', PostCreateView.as_view(), name='post-create'),
]