from django.urls import path
from .views import get_flight

urlpatterns = [
    path("flights/get", get_flight)
]