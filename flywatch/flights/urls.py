from django.urls import path
from .views import get_flight, get_cheapest, get_flights_range

urlpatterns = [
    path("flights/get", get_flight),
    path("flights/cheapest", get_cheapest),
    path("flights/range", get_flights_range)
]