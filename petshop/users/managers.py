from django.contrib.auth.models import BaseUserManager
from django.db import transaction

from .choices import USER_ROLE_ADMIN


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not username:
            raise ValueError('Users must have username.')
        if not email:
            raise ValueError('Users must have email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    @transaction.atomic
    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_active = True
        user.is_superuser = True
        user.role = USER_ROLE_ADMIN
        user.save(using=self._db)
        return user
