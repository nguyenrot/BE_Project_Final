from api_users.models import User


def get_user(*, user: User):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "user": get_user(user=user),
    }
