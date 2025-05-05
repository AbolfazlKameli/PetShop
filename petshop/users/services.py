from random import randint

from decouple import config
from django.core.cache import cache
from kavenegar import KavenegarAPI, HTTPException, APIException

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


def check_otp_code(*, otp_code: str, email: str | None = None, phone_number: str | None = None) -> bool:
    code: str = ''
    if email:
        code = cache.get(f'otp_code_{email}')
    elif phone_number:
        code = cache.get(f'otp_code_{phone_number}')

    if code == otp_code:
        cache.delete(f'otp_code_{email}')
        cache.delete(f'otp_code_{phone_number}')
        cache.delete(f'otp_code_{otp_code}')
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

    for key, value in data:
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
