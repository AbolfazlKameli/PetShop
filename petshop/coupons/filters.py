from datetime import datetime

import django_filters
import pytz
from django.conf import settings

from .models import Coupon


class CouponFilter(django_filters.FilterSet):
    is_valid = django_filters.BooleanFilter(method='filter_is_valid')

    class Meta:
        model = Coupon
        fields = ['code', 'is_valid']

    def filter_is_valid(self, queryset, name, value):
        now = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        if value:
            return queryset.filter(expiration_date__gt=now)
        elif not value:
            return queryset.exclude(expiration_date__gt=now)
        return queryset
