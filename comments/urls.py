from unicodedata import name
from .views import (
    CommentListView
)

from django.urls import path

urlpatterns = [
    path('', CommentListView, name="comments-list")
]
