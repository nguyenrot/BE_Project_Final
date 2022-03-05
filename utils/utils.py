import jwt
from django.conf import settings


class Util:
    @staticmethod
    def HS256_encode(payload):
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256").decode(
            "utf-8"
        )

    @staticmethod
    def HS256_decode(token):
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return "token expired"
        except jwt.exceptions.DecodeError:
            return "token invalid"
