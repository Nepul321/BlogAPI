from django.urls import path
from .views import (
    AccountVerification,
    UserListView,
    RegisterUserView,
    LoginView,
    LogoutView,
    LoggedInUserView,
    ChangePasswordView,
    PasswordResetView,
    PasswordResetFormView
)

urlpatterns = [
    path('', UserListView, name="user-list"),
    path('register/', RegisterUserView, name="user-register"),
    path('login/', LoginView, name="user-login"),
    path('logout/', LogoutView, name="user-logout"),
    path('user/', LoggedInUserView, name="user-logged-in"),
    path('<str:token>/activate/', AccountVerification, name="user-account-activate"),
    path('password/', ChangePasswordView, name="user-password"),
    path('password/reset/', PasswordResetView, name="user-password-reset"),
    path('password/reset/<str:token>/', PasswordResetFormView, name="user-password-reset-form")
]
