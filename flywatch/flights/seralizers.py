from rest_framework import serializers

class FlightSerializer(serializers.Serializer):
    origin = serializers.CharField(max_length=3)
    destination = serializers.CharField(max_length=3)
    max_price = serializers.IntegerField()
    departure_date = serializers.DateField(required=False)
    return_date = serializers.DateField(required=False)

    def validate(self, data):
        departure = data.get("departure_date")
        return_to = data.get("return_date")
        if departure and return_to:
            days_count = (return_to - departure).days + 1

            if days_count <= 0:
                raise serializers.ValidationError("Дата возвращения не может быть раньше даты вылета")
        return data
    
    
class FlightRangeSerializer(serializers.Serializer):
    origin = serializers.CharField(max_length=3)
    destination = serializers.CharField(max_length=3)
    max_price = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    return_date = serializers.DateField(required=False)

    def validate(self, data):
        start = data.get("start_date")
        end = data.get("end_date")

        if start and end:
            days_count = (end-start).days + 1
            if days_count > 7:
                raise serializers.ValidationError("Максимальный диапазон поиска - 7 дней")
            if days_count <= 0:
                raise serializers.ValidationError("Дата завершения поиска не может быть раньше начала")
            
        return data
        