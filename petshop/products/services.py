from django.db import transaction

from .models import Product, ProductCategory


@transaction.atomic
def create_product(data, category: ProductCategory) -> Product:
    return Product.objects.create(**data, category=category)
