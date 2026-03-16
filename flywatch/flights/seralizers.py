from rest_framework import serializers

class FlightSerializer(serializers.Serializer):
    origin = serializers.CharField(max_length=3)
    destination = serializers.CharField(max_length=3)
    max_price = serializers.IntegerField()
    type = serializers.CharField(required=False)
    departure_date = serializers.DateField(required=False)
    return_date = serializers.DateField(required=False)