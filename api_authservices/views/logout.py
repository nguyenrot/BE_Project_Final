from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api_oauth2.services import AuthorizationOauth2


class LogoutView(APIView):
    # logout not need scope
    permission_classes = []

    def post(self, request, *args, **kwargs):
        refresh_token = request.POST.get("refresh_token")
        access_token = request.POST.get("access_token")
        revoke_token = AuthorizationOauth2.logout_oauth2(
            refresh_token, access_token)
        if revoke_token:
            return Response({"message": "logout success!"}, status=status.HTTP_200_OK)
        return Response(
            {"error": "can not revoke access_token or refresh_token"},
            status=status.HTTP_400_BAD_REQUEST,
        )
