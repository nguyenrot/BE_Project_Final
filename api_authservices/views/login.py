from rest_framework import status
from rest_framework.response import Response
from api_base.views import BaseViewSet
from api_authservices.serializers import LoginSerializer
from api_oauth2.services import AuthorizationOauth2
from api_users.models import User


class LoginApi(BaseViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        request_oauth2 = AuthorizationOauth2.authorization_oauth2(
            username, password)
        data = request_oauth2.json()
        if request_oauth2.status_code == 200:
            if User.objects.filter(username=username).first().is_active:
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {"User is not activate"}, status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
