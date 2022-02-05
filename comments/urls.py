from unicodedata import name
from .views import (
    CommentLikeUnlikeView,
    CommentListView,
    PostCommentListView,
    CommentDetailDeleteView
)

from django.urls import path

urlpatterns = [
    path('', CommentListView, name="comments-list"),
    path('post/<int:id>/', PostCommentListView, name="post-comments-list"),
    path('<int:id>/', CommentDetailDeleteView, name="comment-details-delete"),
    path('action/', CommentLikeUnlikeView, name="comments-like-unlike-view"),
]
