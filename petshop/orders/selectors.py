from .models import Order


def get_all_orders() -> list[Order]:
    return Order.objects.all()
