from unicodedata import name
from django.urls import path
from .views import (
    UserListView,
    RegisterUserView,
    LoginView,
    LogoutView,
    LoggedInUserView
)

urlpatterns = [
    path('', UserListView, name="user-list"),
    path('register/', RegisterUserView, name="user-register"),
    path('login/', LoginView, name="user-login"),
    path('logout/', LogoutView, name="user-logout"),
    path('user/', LoggedInUserView, name="user-logged-in")
]
