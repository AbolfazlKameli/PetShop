from django.contrib import admin

from .models import ArticleCategory, Article, ArticleReview


class ArticleReviewInline(admin.TabularInline):
    model = ArticleReview


@admin.register(ArticleCategory)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'id')
    search_fields = ('title',)

    prepopulated_fields = {'slug': ('title',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'updated_date')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'text')

    inlines = (ArticleReviewInline,)


@admin.register(ArticleReview)
class ProductReviewModelAdmin(admin.ModelAdmin):
    list_display = ('article__title', 'owner__username', 'status', 'rate')
    list_filter = ('status', 'rate')
    search_fields = ('body', 'owner__username')
