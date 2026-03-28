from users.models import User
from rest_framework.test import APIClient, APITestCase
from .models import Subscription
from django.urls import reverse


class TestSub(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_A = User.objects.create_user(username="testUserA", password="password")
        self.user_B = User.objects.create_user(username="testUserB", password="password")
        self.client.force_authenticate(user=self.user_A)

        Subscription.objects.create(
            user=self.user_B, origin="TSE", destination="DXB", 
            max_price=1000, start_date="2026-01-01", end_date="2026-01-05", trip_type=Subscription.TripType.ONEWAY
        )


    def test_permissions(self):
        url = reverse("subs-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
    

    def test_create_on_user(self):
        url = reverse("subs-list")

        data = {
            "origin":"ALA", "destination":"DXB", 
            "max_price": 1000, "start_date":"2026-01-01", "end_date":"2026-01-05", "trip_type": Subscription.TripType.ONEWAY
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        sub = Subscription.objects.get(origin="ALA")
        self.assertEqual(sub.user, self.user_A)
