from celery import shared_task
from django.db.models import F
from celery_singleton import Singleton


@shared_task(base=Singleton)
def set_price(subscription_id):
    from .models import Subscription

    subscription = (
        Subscription.objects.filter(id=subscription_id)
        .annotate(
            annotated_price=F("service__full_price")
            - F("service__full_price") * F("plan__discount_percent") / 100.00
        )
        .first()
    )

    subscription.price = subscription.annotated_price
    subscription.save()
