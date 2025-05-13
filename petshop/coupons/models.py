from django.core.validators import MaxValueValidator
from django.db import models

from petshop.utils.utils import BaseModel


class Coupon(BaseModel):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    discount_percent = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)],
        default=0,
        db_index=True
    )
    expiration_date = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ('-created_date',)
