from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *


app_name = 'postapp'

urlpatterns = [
    # path('', cache_page(60)(PostListView.as_view()), name='home'),
    path('', PostListView.as_view(), name='home'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/',PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostUpdateView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('cats/', CategoryListView.as_view(), name='category-list'),
    path('search/', SearchResultView.as_view(), name='post-search'),
    path('cat/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # path('create/', PostCreateView.as_view(), name='post-create'),
]