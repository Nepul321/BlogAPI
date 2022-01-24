from unicodedata import name
from django.urls import path
from .views import (
    UserListView
)

urlpatterns = [
    path('', UserListView, name="user-list")
]
