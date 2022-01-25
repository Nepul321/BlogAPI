from unicodedata import name
from django.urls import path
from .views import (
    UserListView,
    RegisterUserView,
    LoginView
)

urlpatterns = [
    path('', UserListView, name="user-list"),
    path('register/', RegisterUserView, name="user-register"),
    path('login/', LoginView, name="user-login")
]
