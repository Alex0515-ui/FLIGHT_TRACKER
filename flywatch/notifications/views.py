from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated


class NotificationView(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    
