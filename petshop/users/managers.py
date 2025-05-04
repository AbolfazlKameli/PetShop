from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, email, password):
        if not username:
            raise ValueError('Users must have username.')
        if not phone_number:
            raise ValueError('Users must have phone number.')
        if not email:
            raise ValueError('Users must have email')

        user = self.model(username=username, phone_number=phone_number, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, email, password):
        user = self.create_user(username, phone_number, email, password)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
