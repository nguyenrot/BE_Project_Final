import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.conf import settings
from api_users.manages import UserManager
from api_users.models.roles import Role


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, blank=True, max_length=255)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    password = models.CharField(verbose_name="password", max_length=255)
    email = models.EmailField(max_length=255, unique=True, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    roles = models.ManyToManyField(Role, related_name="users", null=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "username"
    objects = UserManager()

    class Meta:
        db_table = "ac_users"

    def __str__(self):
        return str(self.id)

    def set_password(self, raw_password):
        self.password = make_password(
            password=raw_password, salt=settings.SECRET_KEY)
        self._password = raw_password

    def get_full_name(self):
        return self.first_name + " " + self.last_name
