from .models import ProductCategory, Product


def get_all_categories() -> list[ProductCategory]:
    return ProductCategory.objects.all()


def get_all_products() -> list[Product]:
    return Product.objects.select_related('category').all()
