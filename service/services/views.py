from django.conf import settings
from django.core.cache import cache

from django.db.models import Prefetch, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().select_related('client__user').prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().only('client.company_name')),
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_amount = price_cache
        else:
            total_amount = queryset.aggregate(total_amount=Sum('price')).get('total_amount')
            cache.set(settings.PRICE_CACHE_NAME, total_amount, 60)

        response_data = {'result': response.data, 'total_amount': total_amount}
        response.data = response_data
        return response
