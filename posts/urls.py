from unicodedata import name
from django.urls import path
from .views import (
    PostDetailView,
    PostsListView
)

urlpatterns = [
    path('', PostsListView, name="posts-list"),
    path('<id>/', PostDetailView, name="post-details"),
]
