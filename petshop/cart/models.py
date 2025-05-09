from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

from petshop.products.models import Product
from petshop.utils.utils import BaseModel

User = get_user_model()


class Cart(BaseModel):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(100)])
    created_date = models.DateTimeField(auto_now_add=True)
