from api_users.models import User, Role


class UserService:
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
