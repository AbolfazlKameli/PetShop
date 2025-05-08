from .models import User, Address


def get_all_users() -> list[User]:
    users = User.objects.all()
    return users


def get_user_by_phone_number(phone_number: str) -> User | None:
    return User.objects.filter(phone_number=phone_number).first()


def get_user_by_email(email: str) -> User | None:
    return User.objects.filter(email=email).first()


def get_user_by_id(user_id: int) -> User | None:
    return User.objects.filter(id=user_id).prefetch_related('address').first()


def get_all_addresses() -> list[Address]:
    return Address.objects.select_related('owner').all()


def get_user_addresses(owner: User) -> list[Address]:
    return Address.objects.filter(owner=owner)
