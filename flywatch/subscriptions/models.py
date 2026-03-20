from django.db import models
from users.models import User

# Таблица подписки
class Subscription(models.Model):

    class TripType(models.TextChoices):
        ONEWAY = "one_way", "One way"
        ROUND_TRIP = "round_trip", "Round trip"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    max_price = models.PositiveIntegerField()
    trip_type = models.CharField(
        max_length=20, 
        choices=TripType, 
        default=TripType.ONEWAY
    )
    start_date = models.DateField()
    end_date = models.DateField()
    last_notified_price = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)





    