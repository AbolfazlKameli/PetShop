from .models import User


def get_all_users() -> list[User]:
    users = User.objects.all()
    return users


def get_user_by_phone_number(phone_number: str) -> User:
    return User.objects.filter(phone_number=phone_number).first()


def get_user_by_email(email: str) -> User:
    return User.objects.filter(email=email).first()


def get_user_by_id(user_id: int) -> User:
    return User.objects.filter(id=user_id).prefetch_related('address').first()
