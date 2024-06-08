from django.urls import path
from blog.apps import BlogConfig
from blog.views import (BlogArticleCreateView, BlogArticleListView, BlogArticleDetailView, BlogArticleUpdateView,
                        BlogArticleDeleteView)

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogArticleCreateView.as_view(), name='create'),
    path('', BlogArticleListView.as_view(), name='list'),
    path('delete/<int:pk>/', BlogArticleDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', BlogArticleUpdateView.as_view(), name='edit'),
    path('view/<int:pk>/', BlogArticleDetailView.as_view(), name='view'),
]