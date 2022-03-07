from rest_framework import viewsets
from api_users.models import User
from rest_framework.response import Response
from api_users.serializers import UserSerializer, UserRegisterSerializer
from rest_framework import status


class UserView(viewsets.ModelViewSet):
    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
    }
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegisterSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid()
        user = serializer.save()
        serializer_get = UserSerializer(user)
        return Response(serializer_get.data, status=status.HTTP_201_CREATED)
