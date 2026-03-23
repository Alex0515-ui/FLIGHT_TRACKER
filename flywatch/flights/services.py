import requests
from datetime import datetime, timedelta
from subscriptions.models import Subscription
from notifications.models import Notification
import os

API_URL = "https://serpapi.com/search?engine=google_flights"

class FlightService:

    def __init__(self):
        self.url = API_URL
        self.api_key = os.environ.get("SECRET_API_KEY")


    def fetch_flight(self, origin, destination, departure_date, max_price, type, return_date=None):
        if return_date is not None:
            type = 1
        else: 
            type = 2

        data = requests.get(self.url, {
            "api_key": self.api_key,
            "departure_id": origin, 
            "arrival_id": destination, 
            "max_price": max_price,
            "outbound_date": departure_date,
            "currency": "USD",
            "hl": "ru"
        })
        return data.json()
    

    def search_flights_in_range(self, origin, destination, max_price, start_date, end_date, return_date=None):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days_count = (end - start).days + 1
        all_days = [(start + timedelta(days=x)).strftime("%Y-%m-%d") for x in  range(days_count)]

        results = []
        for day in all_days:
            data = self.fetch_flight(
                origin=origin, destination=destination, 
                departure_date=day, max_price=max_price, 
                return_date=return_date
            )

            all_flights = data.get("best_flights", []) + data.get("other_flights", [])
            if all_flights:
                min_price = min(flight["price"] for flight in all_flights)
                results.append({"date": day, "min_price": min_price, "data": data})
        
        results.sort(key=lambda x: x["min_price"])
        return results

        



    
