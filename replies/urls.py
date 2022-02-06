from django.urls import path
from .views import (
    CommentRepliesView,
    ReplyListView
)

urlpatterns = [
    path('', ReplyListView, name="reply-list"),
    path('comment/<int:id>/', CommentRepliesView, name="comment-replies-list")
]
