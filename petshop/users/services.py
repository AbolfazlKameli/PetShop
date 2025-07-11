import hashlib
from random import randint
from typing import Literal

from decouple import config
from django.core.cache import cache
from kavenegar import KavenegarAPI, HTTPException, APIException

from .models import User


def hash_key(cache_key: str) -> str:
    return hashlib.sha256(cache_key.encode()).hexdigest()


def generate_otp_code(
        *,
        email: str | None = None,
        phone_number: str | None = None,
        action: Literal['verify', 'reset_password']
) -> str:
    identifier = email or phone_number
    if not identifier:
        raise ValueError('Email or Phone number must be provided.')

    cache_key = f'otp_code_{hash_key(identifier)}_{action}'

    while True:
        otp_code: str = str(randint(10_000, 99_999))
        if not cache.get(f'otp_used_{otp_code}_{action}'):
            cache.set(cache_key, otp_code, 300)
            cache.set(f'otp_used_{otp_code}_{action}', True, timeout=300)
            return otp_code


def check_otp_code(
        *,
        otp_code: str,
        email: str | None = None,
        phone_number: str | None = None,
        action: Literal['verify', 'reset_password']
) -> bool:
    identifier = email or phone_number
    if not identifier:
        raise ValueError('Email or Phone number must be provided.')

    cache_key = f'otp_code_{hash_key(identifier)}_{action}'
    code = cache.get(cache_key)

    if code == otp_code:
        cache.delete(cache_key)
        cache.delete(f'otp_used_{otp_code}_{action}')
        return code == otp_code
    return False


def register(*, email: str, username: str, password: str) -> User:
    user = User.objects.create_user(email=email, username=username, password=password)
    return user


def activate_user(user: User) -> User:
    user.is_active = True
    user.full_clean()
    user.save()
    return user


def deactivate_user(user: User) -> User:
    user.is_active = False
    user.full_clean()
    user.save()
    return user


def change_user_password(user: User, password: str) -> User:
    user.set_password(password)
    user.full_clean()
    user.save()
    return user


def update_user(user: User, data) -> tuple[str, int]:
    email = data.get('email')
    phone_number = data.get('phone_number')
    email_changed = email and (email != user.email)
    phone_changed = phone_number and (phone_number != user.phone_number)

    for key, value in data.items():
        setattr(user, key, value)
    message = 'Profile updated successfully.'

    if email_changed or phone_changed:
        user.is_active = False
        user.save()
        if email_changed:
            message += ' activation code sent to your new phone number.'
        if phone_changed:
            message += ' activation code sent to you new email address.'
        return message, 1 if email_changed else 2
    user.save()
    return message, 0


def send_sms(*, phone_number: str, content: str):
    api = KavenegarAPI(config('KAVENEGAR_API_KEY'))
    sender = config('KAVENEGAR_PHONE_NUMBER', default='2000500666')
    params = {'sender': sender, 'receptor': phone_number, 'message': content}
    try:
        response = api.sms_send(params)
    except APIException:
        return False
    except HTTPException:
        return False
    return response
