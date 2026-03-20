from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationView

router = DefaultRouter()

router.register(r"notifications", NotificationView, basename="nots")

urlpatterns = [
    path("", include(router.urls)),
]