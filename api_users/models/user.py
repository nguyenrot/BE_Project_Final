import uuid
from api_departments.models import Department
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
    name = models.CharField(max_length=255, blank=True)
    department = models.ForeignKey(Department, related_name="user", null=True, on_delete=models.CASCADE)
    position = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    roles = models.ManyToManyField(Role, related_name="users", null=True)
    birthday = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    avatar = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "username"
    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return str(self.id)

    def set_password(self, raw_password):
        self.password = make_password(
            password=raw_password, salt=settings.SECRET_KEY)
        self._password = raw_password
