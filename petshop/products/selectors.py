from .choices import REVIEW_STATUS_APPROVED
from .models import ProductCategory, Product, ProductDetail, ProductImage, ProductReview


def get_all_categories() -> list[ProductCategory]:
    return ProductCategory.objects.all()


def get_all_products() -> list[Product]:
    return Product.objects.select_related('category').prefetch_related('reviews', 'details', 'images').all()


def get_product_by_id(product_id: int) -> Product | None:
    return Product.objects.filter(id=product_id).first()


def get_detail_by_id(detail_id: int) -> ProductDetail | None:
    return ProductDetail.objects.filter(id=detail_id).first()


def get_primary_image(product: Product) -> ProductImage | None:
    return product.images.filter(is_primary=True).first()


def get_latest_image(product: Product) -> ProductImage | None:
    return product.images.last()


def get_image_by_id(image_id: int) -> ProductImage | None:
    return ProductImage.objects.filter(id=image_id).first()


def get_approved_reviews(product: Product) -> list[ProductReview]:
    return product.reviews.filter(status=REVIEW_STATUS_APPROVED)


def get_review_by_product_and_id(product: Product, review_id: int) -> ProductReview | None:
    return product.reviews.filter(id=review_id).first()
