from unicodedata import name
from django.urls import path
from .views import (
    SubreplylistView
)

urlpatterns = [
    path('', SubreplylistView, name="sub-reply-list-view")
]
