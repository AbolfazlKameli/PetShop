from random import randint

from django.core.cache import cache

from .models import User


def generate_otp_code(*, email: str | None = None, phone_number: str | None = None) -> str:
    while True:
        otp_code: str = str(randint(10000, 99999))
        if not cache.get(f'otp_code_{otp_code}'):
            if phone_number:
                cache.set(f'otp_code_{otp_code}', phone_number, timeout=300)
                cache.set(f'otp_code_{phone_number}', otp_code, timeout=300)
            elif email:
                cache.set(f'otp_code_{otp_code}', email, timeout=300)
                cache.set(f'otp_code_{email}', otp_code, timeout=300)
            return otp_code


def register(*, email: str, username: str, password: str) -> User:
    user = User.objects.create_user(email=email, username=username, password=password)
    return user
