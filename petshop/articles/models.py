from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.utils.text import slugify

from petshop.utils.utils import BaseModel
from .choices import REVIEW_STATUS_CHOICES, REVIEW_STATUS_PENDING, REVIEW_STATUS_APPROVED

User = get_user_model()


class ArticleCategory(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=70, allow_unicode=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-title',)
        verbose_name_plural = 'Categories'


class Article(BaseModel):
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=235)
    slug = models.SlugField(max_length=255, allow_unicode=True)
    text = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def overall_rate(self):
        avg_rate = self.reviews.filter(status=REVIEW_STATUS_APPROVED).aggregate(avg=Avg('rate'))['avg']
        return round(avg_rate, 1) if avg_rate is not None else 0

    class Meta:
        ordering = ('-updated_date',)


class ArticleReview(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_reviews')
    body = models.CharField(max_length=250)
    status = models.CharField(
        max_length=10,
        choices=REVIEW_STATUS_CHOICES,
        default=REVIEW_STATUS_PENDING,
        db_index=True,
        verbose_name='Article Review Status'
    )
    rate = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_date',)
