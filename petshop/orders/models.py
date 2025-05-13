from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from petshop.products.models import Product
from petshop.utils.utils import BaseModel
from petshop.coupons.models import Coupon
from .choices import ORDER_STATUS_CHOICES, ORDER_STATUS_PENDING

User = get_user_model()


class Order(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(
        choices=ORDER_STATUS_CHOICES,
        default=ORDER_STATUS_PENDING,
        max_length=10,
        db_index=True,
        verbose_name='Order Status'
    )
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, related_name='orders', blank=True, null=True)
    discount_percent = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)],
        default=0,
        db_index=True
    )

    class Meta:
        ordering = ('-created_date',)

    def get_total_price(self):
        price = round(
            sum(item.get_total_price() for item in self.items.all())
        )
        if self.discount_percent > 0:
            discount_amount = price * Decimal(self.discount_percent / 100)
            price -= discount_amount
        return round(price)

    def get_total_quantity(self):
        quantity = sum(item.quantity for item in self.items.all())
        return quantity


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(1000)],
        db_index=True,
        default=0
    )

    class Meta:
        ordering = ('-created_date',)

    def clean(self):
        if not self.product.available:
            raise ValidationError('Product is not available.')

        if self.quantity > self.product.quantity:
            raise ValidationError('The quantity you requested is more than what is currently available in stock.')

    def get_total_price(self):
        price = self.product.get_final_price() * self.quantity
        return price
