from unicodedata import name
from .views import (
    HomeView
)

from .api.views import (
    APIBaseView
)

from django.urls import path

urlpatterns = [
    path('', HomeView, name="home"),
    path('api/', APIBaseView, name="api-base-point"),
]
