import requests

API_URL = "https://serpapi.com/search?engine=google_flights"

class FlightService:

    def __init__(self):
        self.url = API_URL
        self.api_key = "f80b0f2770bc4312a6b7a20c24d9e1147e3eac82052102b65c5451aacb874443"

    def get_flight(self, req):
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