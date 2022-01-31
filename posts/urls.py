from django.urls import path
from .views import (
    PostsListView
)

urlpatterns = [
    path('', PostsListView, name="posts-list"),
]
