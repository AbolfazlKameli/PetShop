from django.contrib.auth import get_user_model
from django.db import transaction

from petshop.products.models import Product
from .models import Order, OrderItem

User = get_user_model()


@transaction.atomic
def create_order(owner: User, data: list[dict[str, int | Product]]):
    order = Order.objects.create(owner=owner)

    products_to_update = []
    items = []

    for item in data:
        product = item.get('product')
        quantity = item.get('quantity')

        product.quantity -= quantity
        products_to_update.append(product)

        items.append(OrderItem(order=order, product=product, quantity=quantity))

    Product.objects.bulk_update(products_to_update, ['quantity'])
    OrderItem.objects.bulk_create(items)

    return order
