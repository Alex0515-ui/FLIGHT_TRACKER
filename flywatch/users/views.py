from rest_framework import viewsets
from .models import User
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

class UserView(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    
    

