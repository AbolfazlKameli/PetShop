from django.db import transaction

from petshop.orders.models import Order
from .models import Coupon


@transaction.atomic
def apply_coupon(coupon: Coupon, order: Order) -> Order:
    order.discount_percent += coupon.discount_percent
    order.coupon = coupon
    order.full_clean()
    order.save()
    return order


@transaction.atomic
def discard_coupon(coupon: Coupon, orders: list[Order]):
    for order in orders:
        order.discount_percent -= coupon.discount_percent
        order.coupon = None
    Order.objects.bulk_update(orders, ['discount_percent', 'coupon'])
