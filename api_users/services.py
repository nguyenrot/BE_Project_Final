from typing import Tuple
from django.db import transaction

from api_users.models import User
from utils import get_now


def create_user_google(username, password=None, **extra_fields) -> User:
    if User.objects.filter(username=username).exists():
        return User.objects.filter(username=username).first()
    user = User(username=username, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user


def user_create_superuser(username, password=None, **extra_fields) -> User:
    extra_fields = {**extra_fields, "is_staff": True, "is_superuser": True}

    user = create_user_google(
        username=username, password=password, **extra_fields)

    return user


def user_record_login(*, user: User) -> User:
    user.last_login = get_now()
    user.save()
    return user


@transaction.atomic
def user_get_or_create(*, username: str, **extra_data) -> Tuple[User, bool]:
    user = User.objects.filter(username=username).first()

    if user:
        return user, False

    return create_user_google(username=username, **extra_data), True
