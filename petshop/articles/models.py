from django.db import models
from django.utils.text import slugify

from petshop.utils.utils import BaseModel


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

    class Meta:
        ordering = ('-updated_date',)
