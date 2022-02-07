from unicodedata import name
from django.urls import path
from .views import (
    SubreplylistView,
    ReplySubRepliesView
)

urlpatterns = [
    path('', SubreplylistView, name="sub-reply-list-view"),
    path('replies/<int:id>/', ReplySubRepliesView, name="reply-subreply-view"),
]
