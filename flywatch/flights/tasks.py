from subscriptions.models import Subscription
from .services import FlightService
from notifications.models import Notification
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task # Каждые 6 часов будет запускаться проверка подписок
def check_flight_prices():
    logger.info("Задача запущена")
    subs = Subscription.objects.filter(is_active=True)
    service = FlightService()
    
    for sub in subs:
        user = sub.user
        data = service.search_flights_in_range(
            sub.origin, sub.destination, sub.max_price, 
            sub.start_date, sub.end_date
        )
        logger.info(len(data))

        if len(data) == 0:
            continue
        cheapest_flight = data[0]
        logger.info("Данные найдены")

        if sub.last_notified_price == None:
            sub.last_notified_price = cheapest_flight["min_price"]
            Notification.objects.create(
                user=user, 
                subscription=sub, 
                price=cheapest_flight["min_price"], 
                origin=sub.origin,
                destination=sub.destination,
                flight_date=cheapest_flight["date"]
            )
            logger.info("Уведомление создано")
            sub.save()
        

        elif sub.last_notified_price < cheapest_flight["min_price"]:
            continue

        elif sub.last_notified_price > cheapest_flight["min_price"]:
            sub.last_notified_price = cheapest_flight["min_price"]
            
            Notification.objects.create(
                user=user, 
                subscription=sub, 
                price=cheapest_flight["min_price"], 
                origin=sub.origin, 
                destination=sub.destination,
                flight_date=cheapest_flight["departure_date"]
            )

            sub.save()
            logger.info("Уведомление создано")


