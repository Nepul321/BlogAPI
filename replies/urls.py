from django.urls import path
from .views import (
    CommentRepliesView,
    ReplyDetailDeleteView,
    ReplyListView
)

urlpatterns = [
    path('', ReplyListView, name="reply-list"),
    path('comment/<int:id>/', CommentRepliesView, name="comment-replies-list"),
    path('<int:id>/', ReplyDetailDeleteView, name="reply-detail-view"),
]
