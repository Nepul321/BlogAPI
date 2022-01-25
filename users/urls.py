from unicodedata import name
from django.urls import path
from .views import (
    UserListView,
    RegisterUserView
)

urlpatterns = [
    path('', UserListView, name="user-list"),
    path('register/', RegisterUserView, name="user-register"),
]
