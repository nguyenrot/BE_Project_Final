from time import time
from typing import Tuple
from django.db import transaction

from api_users.models import User, Role

# from api_users.serializers import UserSerializer
from utils import get_now
from utils.utils import Util
from django.conf import settings


class UserService:
    @classmethod
    def create_user_google(cls, username, password=None, **extra_fields) -> User:
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

    @classmethod
    def user_create_superuser(cls, username, password=None, **extra_fields) -> User:
        extra_fields = {**extra_fields, "is_staff": True, "is_superuser": True}

        user = cls.create_user_google(
            username=username, password=password, **extra_fields
        )

        return user

    @classmethod
    def user_record_login(cls, *, user: User) -> User:
        user.last_login = get_now()
        user.save()
        return user

    @classmethod
    @transaction.atomic
    def user_get_or_create(cls, *, username: str, **extra_data) -> Tuple[User, bool]:
        user = User.objects.filter(username=username).first()

        if user:
            return user, False

        return cls.create_user_google(username=username, **extra_data), True

    @classmethod
    def update(cls, instance, validated_data):
        roles = ""
        if "roles" in validated_data:
            roles = validated_data.pop("roles")
        User.objects.filter(pk=instance.id).update(**validated_data)
        if roles:
            roles_list = []
            role_id_list = map(lambda t: t.get("id"), roles)
            roles_list.extend(Role.objects.in_bulk(role_id_list))
            instance.roles.set(roles_list)
        else:
            instance.roles.set([])
        for attrs, value in validated_data.items():
            setattr(instance, attrs, value)
        instance.save()
        return instance

    @staticmethod
    def change_valid_password(data, user):
        curr_pwd = data.get("currentPassword")
        new_pwd = data.get("newPassword")
        password_has_been_set = user.has_usable_password()
        is_correct_password = user.check_password(curr_pwd)
        if password_has_been_set:
            if is_correct_password:
                user.set_password(new_pwd)
                user.save()
                return "success"
            else:
                return "[error] current password incorrect"
        else:
            user.set_password(new_pwd)
            user.save()
            return "success"

    @classmethod
    def activate_user(cls, user):
        user.is_active = True
        user.save()

    @classmethod
    def deactivate_user(cls, user):
        user.is_active = False
        user.save()

    @classmethod
    def check_password(cls, user, password):
        return user.check_password(password)

    @staticmethod
    def forgot_password(email, reset_password_uri):
        user = User.objects.filter(email=email).first()
        if not user:
            return "[error] email invalid"

        reset_password_link = UserService.build_link_reset_password(
            reset_password_uri, user
        )
        logo_uri = reset_password_link.replace(
            "reset-password", "static/paradox-logo-557x450.png"
        )
        send_success = UserService.send_mail_reset_password(
            email, user.get_full_name(), reset_password_link, logo_uri
        )
        return "success" if send_success else "fail"

    @staticmethod
    def build_link_reset_password(uri, user):
        expired_time = settings.RESET_PASSWORD_EXPIRED_TIME  # minute
        payload = {
            "id": str(user.id),
            "username": user.username,
            "exp": time() + 60 * expired_time,
        }
        token = Util.HS256_encode(payload)
        return "{0}?token={1}".format(uri, token)

    # @staticmethod
    # def send_mail_reset_password(email, name, link, logo_uri):
    #     mail_data = {
    #         "template": "mail_templates/api_users/reset_password_mail.html",
    #         "subject": "[Paradox] Reset your password",
    #         "context": {
    #             "name": name,
    #             "link": link,
    #             "logo_uri": logo_uri,
    #         },
    #         "to": [email],
    #     }
    #     return Util.send_html_email(mail_data)
