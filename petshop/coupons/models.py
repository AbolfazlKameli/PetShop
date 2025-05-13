from datetime import datetime

import pytz
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from petshop.utils.utils import BaseModel


class Coupon(BaseModel):
    code = models.SlugField(max_length=50, unique=True, db_index=True)
    discount_percent = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)],
        db_index=True
    )
    expiration_date = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ('-created_date',)

    @property
    def is_valid(self):
        now = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        return now < self.expiration_date

    def clean(self):
        if not self.is_valid:
            raise ValidationError('You can`t choose past time as expiration.')
