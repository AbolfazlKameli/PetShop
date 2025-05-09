from django.contrib.auth import get_user_model
from django.db import models

from petshop.utils.utils import BaseModel

User = get_user_model()


class Cart(BaseModel):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
