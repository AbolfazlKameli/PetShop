from django.db import transaction

from .models import Product, ProductCategory, ProductDetail, ProductReview


@transaction.atomic
def create_product(data, category: ProductCategory) -> Product:
    return Product.objects.create(**data, category=category)


def create_product_details(product: Product, data: dict):
    items = [ProductDetail(**item_data, product=product) for item_data in data]
    ProductDetail.objects.bulk_create(items)


def change_review_status(review: ProductReview, status: str) -> ProductReview:
    review.status = status
    review.save()
    return review
