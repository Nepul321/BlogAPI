from unicodedata import name
from django.urls import path
from .views import (
    CommentRepliesView,
    ReplyDetailDeleteView,
    ReplyListView,
    ReplyLikeUnlikeView,
    ReplyCreateView
)

urlpatterns = [
    path('', ReplyListView, name="reply-list"),
    path('comment/<int:id>/', CommentRepliesView, name="comment-replies-list"),
    path('<int:id>/', ReplyDetailDeleteView, name="reply-detail-view"),
    path('action/', ReplyLikeUnlikeView, name="reply-like-unlike-view"),
    path('create/', ReplyCreateView, name="reply-create-view"),
]
