from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from petshop.utils.utils import BaseModel
from . import choices
from .managers import UserManager
from .validators import validate_iranian_phone_number, validate_postal_code


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='first name')
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='last name')
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(
        validators=[validate_iranian_phone_number],
        max_length=11,
        unique=True,
        verbose_name='phone number',
        blank=True,
        null=True
    )
    email = models.EmailField(unique=True, max_length=50, db_index=True)
    role = models.CharField(
        choices=choices.USER_ROLE_CHOICES,
        default=choices.USER_ROLE_CUSTOMER,
        max_length=10
    )
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username} - {self.email}'

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_customer(self):
        return self.role == choices.USER_ROLE_CUSTOMER

    @property
    def is_admin(self):
        return self.role == choices.USER_ROLE_ADMIN

    class Meta:
        ordering = ('-created_date',)


class Address(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    address = models.TextField()
    postal_code = models.CharField(
        verbose_name='postal code',
        max_length=10,
        validators=[validate_postal_code]
    )

    def __str__(self):
        return f'{self.owner} - {self.postal_code}'

    class Meta:
        ordering = ('-created_date',)
        verbose_name_plural = 'Addresses'
