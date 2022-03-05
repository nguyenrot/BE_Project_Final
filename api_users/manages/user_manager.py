from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_superuser=False):
        if not username:
            raise ValueError("User must have an username")
        if not password:
            raise ValueError("User must have an password")
        user_obj = self.model(username=username)
        user_obj.is_superuser = is_superuser
        user_obj.set_password(password)  # change user password
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, username, password=None):
        user_obj = self.create_user(
            username, password=password, is_superuser=True)
        return user_obj
