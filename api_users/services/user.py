from time import time
from typing import Tuple
from django.db import transaction
from api_admin.models import Invite
from api_users.models import User, LinkingAccount, AuthenticationProvider, Role

# from api_users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from utils import get_now
from api_admin.utils import Util
from django.conf import settings


class UserService:
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
