from rest_framework.test import APIClient, APITestCase
from users.models import User
from .models import Notification
from django.urls import reverse
from subscriptions.models import Subscription


class NotificationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_A = User.objects.create_user(username="testUserA", password="password")
        self.user_B = User.objects.create_user(username="testUserB", password="password")

        self.sub = Subscription.objects.create(
            user=self.user_B, origin="ALA", destination="TSE", 
            max_price=1000, start_date="2026-04-01", end_date="2026-01-06", trip_type=Subscription.TripType.ONEWAY
        )
        
        self.notification = Notification.objects.create(
            user=self.user_B, 
            subscription=self.sub,
            
            price=5000, 
            origin="ALA", 
            destination="TSE",
            flight_date="2026-04-05"
        )

    def test_permissions(self):
        self.client.force_authenticate(user=self.user_A)
        url = reverse("nots-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_auth(self):
        url = reverse("nots-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)


