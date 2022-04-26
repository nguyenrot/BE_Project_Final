from rest_framework import viewsets
from api_users.models import User
from api_users.services import UserService
from rest_framework.response import Response
from api_users.serializers import UserSerializer, UserRegisterSerializer, ChangePasswordSerializer
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
        "change_password": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "active": [["admin"], ["super_admin"]],
        "de_active": [["admin"], ["super_admin"]],
    }
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return UserRegisterSerializer
        if self.action in ("active", "de_active"):
            return None
        if self.action in ("change_password"):
            return ChangePasswordSerializer
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

    @action(detail=False, methods=["PATCH"])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = UserService.change_valid_password(
            serializer.data, request.user)
        status_code = {
            "success": status.HTTP_200_OK,
            "[error] current password incorrect": status.HTTP_406_NOT_ACCEPTABLE,
        }
        return Response({"msg": message}, status=status_code.get(message))
