from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

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
