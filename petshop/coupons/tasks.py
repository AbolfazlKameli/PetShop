from celery import shared_task

from .selectors import get_invalid_coupons
from .services import discard_coupon


@shared_task
def discard_expired_tokens():
    invalid_coupons = get_invalid_coupons()
    if invalid_coupons:
        for coupon in invalid_coupons:
            discard_coupon(coupon, coupon.orders.all())
