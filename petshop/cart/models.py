from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from petshop.products.models import Product
from petshop.utils.utils import BaseModel

User = get_user_model()


class Cart(BaseModel):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def get_overall_price(self):
        price = round(sum(item.product.final_price for item in self.items.all()))
        return price

    def get_overall_quantity(self):
        quantity = sum(item.quantity for item in self.items.all())
        return quantity


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(100)])
    created_date = models.DateTimeField(auto_now_add=True)

    def get_overall_price(self):
        price = self.product.final_price * self.quantity
        return price

    def clean(self):
        if self.product.quantity < self.quantity:
            raise ValidationError('The quantity you requested is more than what is currently available in stock.')
