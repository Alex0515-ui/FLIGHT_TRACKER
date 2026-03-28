from rest_framework.test import APIClient, APITestCase
from unittest.mock import patch
from users.models import User

class Flight_View_Test(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testUser", password="password")
        self.login = self.client.force_authenticate(user=self.user)

    @patch("flights.views.flight_service.fetch_flight")
    def test_fetch_success(self, mock):
        mock.return_value = {"flights": []}
        response = self.client.get("/api/flights/get", {
            "origin": "ALA", "destination": "TSE", "max_price": 5000, "departure_date": "2026-04-05"
        })
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, mock.return_value)
    
    @patch("flights.views.flight_service.fetch_flight")
    def test_fetch_fail(self, mock):
        response = self.client.get("/api/flights/get", {
            "origin": "ALA", "destination": "TSE", "max_price": 5000, 
            "departure_date": "2026-04-05", "return_date": "2026-04-03"
        })
        print(response.content)

        self.assertEqual(response.status_code, 400)
    
    @patch("flights.views.flight_service.fetch_flight")
    def test_range_success(self, mock):
        mock.return_value = {"best_flights": [], "other_flights": []}
        response = self.client.get("/api/flights/range", {
            "origin": "ALA", "destination": "TSE", "start_date": "2026-04-05", 
            "end_date": "2026-04-11", "max_price": 5000
        })
        print(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    @patch("flights.views.flight_service.fetch_flight")
    def test_range_fail(self, mock):
        response = self.client.get("/api/flights/range", {
            "origin": "ALA", "destination": "TSE", "start_date": "2026-04-05", 
            "end_date": "2026-04-03", "max_price": 5000
        })
        print(response.content)

        self.assertEqual(response.status_code, 400)

        