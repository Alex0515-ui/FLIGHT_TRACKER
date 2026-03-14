from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubView

router = DefaultRouter()
router.register('subscriptions', SubView, basename="subs")

urlpatterns = [
    path("", include(router.urls))
]