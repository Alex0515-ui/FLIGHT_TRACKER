from django.db import models
from users.models import User
from subscriptions.models import Subscription

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    flight_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)