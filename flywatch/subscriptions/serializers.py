from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Subscription
        fields = "__all__"
    
    def validate(self, data): # Проверки валидации небольшие
        if data['trip_type'] == Subscription.TripType.ONEWAY and data.get('return_date'):
            raise serializers.ValidationError("One-way trip should not have return date!")
        if data['trip_type'] == Subscription.TripType.ROUND_TRIP and not data.get('return_date'):
            raise serializers.ValidationError("Round trip requires return date")
        return data