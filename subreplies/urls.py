from unicodedata import name
from django.urls import path
from .views import (
    SubReplyDetailDeleteView,
    SubreplylistView,
    ReplySubRepliesView,
    SubReplyLikeUnlikeView
)

urlpatterns = [
    path('', SubreplylistView, name="sub-reply-list-view"),
    path('replies/<int:id>/', ReplySubRepliesView, name="reply-subreply-view"),
    path('<int:id>/', SubReplyDetailDeleteView, name="sub-reply-detail-delete-view"),
    path('action/', SubReplyLikeUnlikeView, name="sub-reply-like-unlike-view"),
]
