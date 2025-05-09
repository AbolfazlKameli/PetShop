from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.StackedInline):
    model = CartItem


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('owner__username', 'id')
    search_fields = ('owner__username',)

    inlines = (CartItemInline,)


@admin.register(CartItem)
class CartItemModelAdmin(admin.ModelAdmin):
    list_display = ('cart__id', 'product__title', 'quantity', 'id')
    search_fields = ('product_title',)
