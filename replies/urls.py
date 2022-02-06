from django.urls import path
from .views import (
    ReplyListView
)

urlpatterns = [
    path('', ReplyListView, name="reply-list"),
]
