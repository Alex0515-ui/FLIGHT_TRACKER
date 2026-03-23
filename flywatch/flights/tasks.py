from subscriptions.models import Subscription
from .services import FlightService
from notifications.models import Notification


def check_flight_prices():
    subs = Subscription.objects.filter(is_active=True)
    service = FlightService()
    
    for sub in subs:
        user = sub.user
        data = service.search_flights_in_range(
            sub.origin, sub.destination, sub.max_price, 
            sub.start_date, sub.end_date
        )

        if len(data) == 0:
            continue
        cheapest_flight = data[0]

        if sub.last_notified_price == None:
            sub.last_notified_price = cheapest_flight["price"]
            Notification.objects.create(
                user=user, 
                subscription=sub, 
                price=cheapest_flight["price"], 
                origin=sub.origin,
                destination=sub.destination,
                flight_date=cheapest_flight["departure_date"]
            )
            sub.save()

        elif sub.last_notified_price < cheapest_flight["price"]:
            continue

        elif sub.last_notified_price > cheapest_flight["price"]:
            sub.last_notified_price = cheapest_flight["price"]
            Notification.objects.create(
                user=user, 
                subscription=sub, 
                price=cheapest_flight["price"], 
                origin=sub.origin, 
                destination=sub.destination,
                flight_date=cheapest_flight["departure_date"]
            )
            sub.save()