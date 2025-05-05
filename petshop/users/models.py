from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from . import choices
from .managers import UserManager
from .validators import validate_iranian_phone_number


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
