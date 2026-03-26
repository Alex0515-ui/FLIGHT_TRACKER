import requests
from datetime import timedelta
import os
import logging
from django.core.cache import cache
logger = logging.getLogger(__name__)
API_URL = "https://serpapi.com/search?engine=google_flights"

class FlightService:

    def __init__(self):
        self.url = API_URL
        self.api_key = os.environ.get("SECRET_API_KEY")


    def fetch_flight(self, origin, destination, departure_date, max_price, return_date=None):
        key = f"flight:{origin}:{destination}:{str(departure_date)}:{max_price}:{return_date}"
        cached_data = cache.get(key)

        if cached_data:
            print("Данные взяты из кэша", flush=True)
            return cached_data
        
        type = 1 if return_date else 2
        params = {
            "api_key": self.api_key,
            "departure_id": origin, 
            "arrival_id": destination, 
            "max_price": max_price,
            "outbound_date": departure_date,
            "type": type,
            "currency": "USD",
            "hl": "ru"
        }

        if return_date:
            params["return_date"] = return_date
        
        data = requests.get(self.url, params)
        response = data.json()
        cache.set(key, response, timeout=300)       # Сохраняем в кэш данные на 5 минут
        return response
    

    def search_flights_in_range(self, origin, destination, max_price, start_date, end_date, return_date=None):
        days_count = (end_date - start_date).days + 1
        
        all_days = [(start_date + timedelta(days=x)).strftime("%Y-%m-%d") for x in  range(days_count)]

        results = []
        for day in all_days:
            data = self.fetch_flight(
                origin=origin, destination=destination, 
                departure_date=day, max_price=max_price, 
                return_date=return_date
            )

            all_flights = data.get("best_flights", []) + data.get("other_flights", [])
            logger.info(f"Найдено рейсов: {len(all_flights)}")
            if all_flights:
                min_price = min(flight["price"] for flight in all_flights)
                results.append({"date": day, "min_price": min_price, "data": data})
        
        results.sort(key=lambda x: x["min_price"])
        return results

        



    
