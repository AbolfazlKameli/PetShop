from .models import ArticleCategory


def get_all_categories() -> list[ArticleCategory]:
    return ArticleCategory.objects.all()
