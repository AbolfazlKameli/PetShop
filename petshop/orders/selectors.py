from .choices import ORDER_STATUS_PENDING
from .models import Order


def get_all_orders() -> list[Order]:
    return Order.objects.select_related('coupon').prefetch_related('items').all()


def get_pending_orders() -> list[Order]:
    return (Order.objects.select_related('coupon')
            .prefetch_related('coupon')
            .select_for_update()
            .filter(status=ORDER_STATUS_PENDING))


def get_order_by_id(order_id: int, for_update: bool = False) -> Order:
    if for_update:
        return Order.objects.prefetch_related('items').filter(id=order_id).select_for_update().first()
    return Order.objects.prefetch_related('items').filter(id=order_id).first()


def check_order_status(order: Order, statuses: list) -> bool:
    return order.status in statuses


def nothing_orders():
    return Order.objects.none()
