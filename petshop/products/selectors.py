from .models import ProductCategory, Product


def get_all_categories() -> list[ProductCategory]:
    return ProductCategory.objects.all()


def get_all_products() -> list[Product]:
    return Product.objects.select_related('category').all()


def get_product_by_id(product_id: int) -> Product:
    return Product.objects.filter(id=product_id).first()
