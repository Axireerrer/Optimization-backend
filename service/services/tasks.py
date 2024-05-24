import datetime
import time

from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.db.models import F
from celery_singleton import Singleton

from django.core.cache import cache


@shared_task(base=Singleton)
def set_price(sub_id):
    from services.models import Subscription
    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().filter(id=sub_id).annotate(
            annotated_price=(F('service__full_price') - (F('service__full_price') * F('plan__discount_percent') / 100))
        ).first()
        subscription.price = subscription.annotated_price
        subscription.save()
    print("Something another logic python from block of set_price")
    cache.delete(settings.PRICE_CACHE_NAME)


@shared_task
def set_comment(sub_id):
    from services.models import Subscription
    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(id=sub_id)
        subscription.comment = str(datetime.datetime.now())
        subscription.save()
    print("Something another logic python from block of set_comment")
    cache.delete(settings.PRICE_CACHE_NAME)