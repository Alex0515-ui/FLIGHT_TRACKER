import requests
from datetime import datetime, timedelta

API_URL = "https://serpapi.com/search?engine=google_flights"

class FlightService:

    def __init__(self):
        self.url = API_URL
        self.api_key = "78f720c0761eb6e336a8c3fac311ab257f2b2d69eb1b20850c443937d2c90c80"


    def fetch_flight(self, req):
        params = {
            "api_key": self.api_key,
            "departure_id": req['origin'], 
            "arrival_id": req['destination'], 
            "max_price": req['max_price'],
            "outbound_date": req["departure_date"],
            "currency": "USD",
            "hl": "ru"
        }
        if req.get('return_date'):
            params["type"] = 1
            params["return_date"] = req['return_date']
        else: 
            params['type'] = 2

        data = requests.get(self.url, params)
        return data.json()
    

    def search_flights_in_range(self, req):
        start = req["start_date"]
        end = req["end_date"]
        days_count = (end - start).days + 1
        all_days = [(start + timedelta(days=x)).strftime("%Y-%m-%d") for x in  range(days_count)]

        results = []
        for day in all_days:
            request = req.copy()
            request["departure_date"] = day

            data = self.fetch_flight(request)
            
            all_flights = data.get("best_flights", []) + data.get("other_flights", [])
            if all_flights:
                min_price = min(flight["price"] for flight in all_flights)
                results.append({"date": day, "min_price": min_price, "data": data})
        
        results.sort(key=lambda x: x["min_price"])
        return results


    def get_cheapest_flight(self, req):
        data = self.fetch_flight(req)

        all_flights = data.get("best_flights", []) + data.get("other_flights", [])
        if not all_flights:
            return None
        
        cheapest_flight = min([f for f in all_flights], key=lambda x: x["price"])
        return cheapest_flight["price"]
        
    
