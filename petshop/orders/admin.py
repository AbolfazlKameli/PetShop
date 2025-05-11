from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('owner__username', 'status', 'discount_percent', 'created_date')
    list_filter = ('status',)
    search_fields = ('owner__username',)
