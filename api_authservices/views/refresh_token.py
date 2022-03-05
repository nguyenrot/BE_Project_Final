from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api_oauth2.services import AuthorizationOauth2


class RefreshTokenView(APIView):
    # Refresh token not need scope
    permission_classes = []

    def post(self, request, *args, **kwargs):
        refresh_token = request.POST.get("refresh_token")
        r = AuthorizationOauth2.refresh_token_view(str(refresh_token))
        data = r.json()
        if r.status_code == 200:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
