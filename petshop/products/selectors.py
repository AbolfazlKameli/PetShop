from .models import ProductCategory, Product, ProductDetail, ProductImage


def get_all_categories() -> list[ProductCategory]:
    return ProductCategory.objects.all()


def get_all_products() -> list[Product]:
    return Product.objects.select_related('category').all()


def get_product_by_id(product_id: int) -> Product | None:
    return Product.objects.filter(id=product_id).first()


def get_detail_by_id(detail_id: int) -> ProductDetail | None:
    return ProductDetail.objects.filter(id=detail_id).first()


def get_primary_image(product: Product) -> ProductImage | None:
    return product.images.filter(is_primary=True).first()


def get_latest_image(product: Product) -> ProductImage | None:
    return product.images.last()
