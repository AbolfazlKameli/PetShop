from .models import ProductCategory


def get_all_categories() -> list[ProductCategory]:
    return ProductCategory.objects.all()
