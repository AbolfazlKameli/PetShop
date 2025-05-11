from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('owner__username', 'status', 'discount_percent', 'created_date')
    list_filter = ('status',)
    search_fields = ('owner__username', 'owner__email')

    inlines = (OrderItemInline,)


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ('order', 'product__title', 'quantity', 'created_date')
    search_fields = ('product__title',)
