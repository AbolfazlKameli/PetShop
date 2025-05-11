from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

from petshop.products.models import Product
from petshop.utils.utils import BaseModel
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
    discount_percent = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)],
        default=0,
        db_index=True
    )

    class Meta:
        ordering = ('-created_date',)


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
