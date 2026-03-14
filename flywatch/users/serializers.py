from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'username': {'min_length': 3}, 
            'password': {'write_only': True, 'min_length': 3}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



