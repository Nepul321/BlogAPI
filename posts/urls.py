from unicodedata import name
from django.urls import path
from .views import (
    PostCreateView,
    PostDetailView,
    PostsListView,
    PostLikeUnlikeView
)

urlpatterns = [
    path('', PostsListView, name="posts-list"),
    path('<int:id>/', PostDetailView, name="post-details"),
    path('create/', PostCreateView, name="post-create"),
    path('action/', PostLikeUnlikeView, name="post-action"),
]
