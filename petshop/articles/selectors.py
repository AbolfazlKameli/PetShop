from .models import Article


def get_all_articles() -> list[Article]:
    return Article.objects.all()
