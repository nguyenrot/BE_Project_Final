from rest_framework import viewsets
from api_users.models import User
from rest_framework.response import Response
from api_users.serializers import UserSerializer, UserRegisterSerializer
from rest_framework import status
from rest_framework.decorators import action


class UserView(viewsets.ModelViewSet):
    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
        "my_info": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "active": [["admin"], ["super_admin"]],
        "de_active": [["admin"], ["super_admin"]],
    }
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return UserRegisterSerializer
        if self.action in ("active", "de_active"):
            return None
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer_get = UserSerializer(user)
        return Response(serializer_get.data, status=status.HTTP_201_CREATED)

    @action(methods=['patch'], detail=True)
    def active(self, request, pk=None):
        user = User.objects.get(pk=pk)
        user.is_active = True
        user.save()
        return Response("Kích hoạt thành công!")

    @action(methods=['patch'], detail=True)
    def de_active(self, request, pk=None):
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return Response("Hủy kích hoạt thành công!")

    @action(methods=['get'], detail=False)
    def my_info(self, request):
        user = request.user
        serializer_get = UserSerializer(user)
        return Response(serializer_get.data)
