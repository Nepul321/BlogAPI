from unicodedata import name
from django.urls import path
from .views import (
    UserListView,
    RegisterUserView,
    LoginView,
    LogoutView
)

urlpatterns = [
    path('', UserListView, name="user-list"),
    path('register/', RegisterUserView, name="user-register"),
    path('login/', LoginView, name="user-login"),
    path('logout/', LogoutView, name="user-logout")
]
