from django.contrib import admin

from .models import Cart


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('owner__username', 'id')
    search_fields = ('owner__username',)
