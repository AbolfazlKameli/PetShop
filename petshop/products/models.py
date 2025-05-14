from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.db import models
from django.db.models import Avg
from django.utils.text import slugify

from petshop.utils.utils import BaseModel
from .choices import REVIEW_STATUS_CHOICES, REVIEW_STATUS_PENDING

User = get_user_model()


class ProductCategory(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=70, allow_unicode=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-title',)
        verbose_name_plural = 'Categories'


class Product(BaseModel):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=70)
    slug = models.SlugField(max_length=100, allow_unicode=True, db_index=True)
    quantity = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(1000)],
        db_index=True,
        default=0
    )
    description = models.TextField()
    available = models.BooleanField(default=True, db_index=True)
    unit_price = models.DecimalField(
        decimal_places=0,
        max_digits=15,
        db_index=True
    )
    discount_percent = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)],
        default=0,
        db_index=True
    )
    final_price = models.DecimalField(
        decimal_places=0,
        max_digits=15,
        default=0,
        db_index=True,
    )

    def get_final_price(self):
        if self.discount_percent > 0:
            discount_amount = self.unit_price * Decimal(self.discount_percent / 100)
            discounted_amount = self.unit_price - discount_amount
            return round(discounted_amount)
        else:
            return round(self.unit_price)

    @property
    def overall_rate(self):
        avg_rate = self.reviews.aggregate(avg=Avg('rate'))['avg']
        return round(avg_rate, 1) if avg_rate is not None else 0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.final_price = self.get_final_price()
        self.available = True if self.quantity > 0 else False
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-updated_date',)


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='details')
    key = models.CharField(max_length=250)
    value = models.CharField(max_length=250)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    is_primary = models.BooleanField(default=False)


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')
    body = models.CharField(max_length=250)
    status = models.CharField(
        max_length=10,
        choices=REVIEW_STATUS_CHOICES,
        default=REVIEW_STATUS_PENDING,
        db_index=True,
        verbose_name='Product Review Status'
    )
    rate = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_date',)
