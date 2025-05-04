from .models import User


def get_all_users() -> list[User]:
    users = User.objects.all()
    return users
