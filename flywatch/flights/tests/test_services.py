from django.test import TestCase, override_settings
from unittest.mock import MagicMock, patch
from django.core.cache import cache
from flights.services import FlightService
from requests.exceptions import RequestException
from requests.exceptions import HTTPError


@override_settings(   # Тестовое хранилище кэша
    CACHES = {
        'default': 
            {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}
    })
class FlightServiceTest(TestCase):

    def setUp(self):
        self.service = FlightService()
        cache.clear()

    @patch("requests.get")
    def test_success_fetch(self, mock):         # Проверяем что запрос к API идет корректно
        mock_response = MagicMock()
        mock_response.json.return_value = {"best_flights": [{"price": 100}]}
        mock_response.status_code = 200
        mock.return_value = mock_response

        result = self.service.fetch_flight("ALA", "TSE", "2026-04-05", 5000)

        args, kwargs = mock.call_args
        self.assertEqual(args[1]["type"], 2)

        self.assertEqual(result["best_flights"][0]["price"], 100)
        mock.assert_called_once()

    @patch("requests.get")
    def test_success_cache_and_logic_fetch(self, mock):       # Проверяем что кэш и type правильно работают
        mock_response = MagicMock()
        mock_response.json.return_value = {"best_flights": [{"price": 100}]}
        mock_response.status_code = 200
        mock.return_value = mock_response

        result = self.service.fetch_flight("ALA", "TSE", "2026-04-05", 5000, "2026-04-10")
        
        args, kwargs = mock.call_args
        self.assertEqual(args[1]["type"], 1)

        result2 = self.service.fetch_flight("ALA", "TSE", "2026-04-05", 5000, "2026-04-10")

        self.assertEqual(mock.call_count, 1)
        self.assertEqual(result["best_flights"][0]["price"], 100)
        mock.assert_called_once()

    @patch("requests.get")
    def fail_retry_success_test(self, mock):
        
        mock.side_effect = [            # Успех только с 3 попытки
            RequestException("Timeout"),
            RequestException("Connection Error"),
            MagicMock(status_code=200, json=lambda: {"best_flights": []})
        ]
        result = self.service.fetch_flight("ALA", "TSE", "2026-04-05", 5000)

        self.assertEqual(result, {"best_flights": []})
        self.assertEqual(mock.call_count, 3)

    @patch("requests.get")
    def test_fail_retry(self, mock):        # Проверям что retry окончательно выбросит ошибку после 4-х раз
        mock.side_effect = RequestException("API is dead")

        with self.assertRaises(RequestException):
            self.service.fetch_flight("ALA", "TSE", "2026-04-05", 25000)

        self.assertEqual(mock.call_count, 4)

    @patch("requests.get")
    def test_fail_http(self, mock):         # Проверяем raise_for_status
        mock_error = MagicMock()
        mock_error.status_code = 500
        mock_error.raise_for_status.side_effect = HTTPError("Server error")
        mock.return_value = mock_error
        
        with self.assertRaises(HTTPError):
            self.service.fetch_flight("ALA", "TSE", "2026-04-05", 5000)
        
    



    

    

    
    
