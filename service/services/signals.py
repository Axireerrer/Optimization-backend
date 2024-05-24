from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.cache import cache

from services.models import Subscription


@receiver(post_delete, sender=Subscription)
def delete_cache_total_sum(instance, *args, **kwargs):
    cache.delete(settings.PRICE_CACHE_NAME)