from unittest.mock import patch
from rest_framework.test import APIClient, APITestCase
from users.models import User
from subscriptions.models import Subscription
from notifications.models import Notification
from flights.tasks import check_flight_prices


class TaskTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testUser', password="password")
        self.login = self.client.force_authenticate(user=self.user)
        self.sub = Subscription.objects.create(
            user=self.user, 
            origin="ALA", 
            destination="TSE", 
            max_price=5000, 
            trip_type=Subscription.TripType.ONEWAY, 
            start_date="2026-04-05", 
            end_date="2026-04-11",
        )

    @patch("flights.services.FlightService.search_flights_in_range")
    def test_success_celery(self, mock):
        mock.return_value = [{"min_price": 5000, "date": "2026-04-06"}]

        check_flight_prices()

        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.price, 5000)
        self.sub.refresh_from_db()
        self.assertEqual(self.sub.last_notified_price, 5000)

    
    @patch("flights.services.FlightService.search_flights_in_range")
    def test_success_celery_price(self, mock):
        self.sub.last_notified_price = 5000
        self.sub.save()
        mock.return_value = [{"min_price": 3000, "date": "2026-04-06"}]
        
        check_flight_prices()

        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.price, 3000)
        self.assertEqual(notification.user, self.user)
        self.sub.refresh_from_db()
        self.assertEqual(self.sub.last_notified_price, 3000)


    @patch("flights.services.FlightService.search_flights_in_range")
    def test_success_celery_no_notification(self, mock):
        self.sub.last_notified_price = 3000
        self.sub.save()
        mock.return_value = [{"min_price": 5000, "date": "2026-04-06"}]

        check_flight_prices()

        self.assertEqual(Notification.objects.count(), 0)
        self.assertEqual(self.sub.last_notified_price, 3000)

    @patch("flights.services.FlightService.search_flights_in_range")
    def test_celery_active(self, mock):
        self.sub.is_active=False
        self.sub.save()
        
        check_flight_prices()

        mock.assert_not_called()
        self.assertEqual(Notification.objects.count(), 0)

    @patch("flights.services.FlightService.search_flights_in_range")
    def test_no_celery_data(self, mock):
        mock.return_value = []
        check_flight_prices()

        mock.assert_called_once()
        self.assertEqual(Notification.objects.count(), 0)

        



    