from unicodedata import name
from .views import (
    CommentListView,
    PostCommentListView
)

from django.urls import path

urlpatterns = [
    path('', CommentListView, name="comments-list"),
    path('post/<int:id>/', PostCommentListView, name="post-comments-list")
]
