from datetime import datetime

import pytz
from django.conf import settings

from .models import Coupon


def get_all_coupons() -> list[Coupon]:
    return Coupon.objects.prefetch_related('orders').all()


def get_valid_coupons() -> list[Coupon]:
    now = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    return Coupon.objects.prefetch_related('orders').filter(expiration_date__gt=now)
