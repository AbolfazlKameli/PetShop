from .models import Order


def get_all_orders() -> list[Order]:
    return Order.objects.all()


def get_order_by_id(order_id: int) -> Order:
    return Order.objects.prefetch_related('items').filter(id=order_id).first()


def check_order_status(order: Order, statuses: list) -> bool:
    return order.status in statuses
