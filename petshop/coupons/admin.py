from django.contrib import admin

from .models import Coupon


@admin.register(Coupon)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'expiration_date', 'id', 'discount_percent')
    search_fields = ('code',)
