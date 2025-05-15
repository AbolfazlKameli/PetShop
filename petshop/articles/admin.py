from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'id')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
