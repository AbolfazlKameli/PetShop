from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify

from petshop.utils.utils import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=230, unique=True)
    slug = models.SlugField(max_length=255, allow_unicode=True)
    text = models.TextField()
    image = models.ImageField(validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    class Meta:
        ordering = ('-updated_date',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
