from django.contrib import admin

from .models import ArticleCategory, Article


@admin.register(ArticleCategory)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'id')
    search_fields = ('title',)

    prepopulated_fields = {'slug': ('title',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'updated_date')
    prepopulated_fields = {'slug': ('title',)}
