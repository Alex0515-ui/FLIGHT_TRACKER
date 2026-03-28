from django.test import TestCase
from unittest.mock import MagicMock, patch
from flights.seralizers import FlightSerializer, FlightRangeSerializer

# ТЕСТЫ НА ОБЫЧНЫЙ ПОИСК РЕЙСОВ
class FlightSerializerTest(TestCase):

    def setUp(self):
        self.base_data = {
            "origin": "ALA",
            "destination": "DBX",
            "max_price": 50000,
            "departure_date": "2026-04-01"
        }
    
    def test_success_trip(self):   # Успешная валидация
        data = self.base_data.copy()
        data["return_date"] = "2026-04-10"
        serializer = FlightSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_fail_trip(self):      # Ошибка при неверной дате возвращения
        data = self.base_data.copy()
        data["return_date"] = "2026-03-29"
        serializer = FlightSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0], 
            "Дата возвращения не может быть раньше даты вылета"
        )

    def test_success_one_way(self): # Успешная валидация в одностороннем рейсе
        data = self.base_data.copy()
        serializer = FlightSerializer(data=data)
        self.assertTrue(serializer.is_valid())


# ТЕСТЫ НА ПОИСК В ДИАПАЗОНЕ
class FlightRangeSerializerTest(TestCase):

    def setUp(self):
        self.range_base_data = {
            "origin": "ALA",
            "destination": "DBX",
            "max_price": 50000,
            "start_date": "2026-04-01",
        }
    
    def test_success_range(self):    # Успешная валидация на получение данных в диапазоне
        data = self.range_base_data.copy()
        data["end_date"] = "2026-04-03"
        serializer = FlightRangeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_fail_range(self):       # Ошибка если превысил лимит диапазона
        data = self.range_base_data.copy()
        data["end_date"] = "2026-04-11"
        serializer = FlightRangeSerializer(data=data)
        self.assertFalse(serializer.is_valid())    
        self.assertEqual(
            serializer.errors["non_field_errors"][0], 
            "Максимальный диапазон поиска - 7 дней"
        )

    def test_second_fail_range(self): # Ошибка если неправильный диапазон
        data = self.range_base_data.copy()
        data["end_date"] = "2026-03-29"
        serializer = FlightRangeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Дата завершения поиска не может быть раньше начала"
        )
    

