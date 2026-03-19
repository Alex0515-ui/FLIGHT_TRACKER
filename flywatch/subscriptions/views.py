from rest_framework import viewsets
from .models import Subscription
from .serializers import SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated

class SubView(viewsets.ModelViewSet):

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): # Чтобы пользователь не мог создавать подписку за другого
        return Subscription.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):  # Подставляем пользователя автоматический
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return 