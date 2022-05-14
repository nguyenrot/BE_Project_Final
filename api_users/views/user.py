from rest_framework import viewsets
from api_users.models import User
from api_users.services import UserService
from rest_framework.response import Response
from api_users.serializers import (UserSerializer, UserRegisterSerializer, ChangePasswordSerializer,
                                   ForgotPasswordSerializer, TokenSerializer, PasswordSerializer)
from rest_framework import status
from rest_framework.decorators import action
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
from api_base.services import SendMail
from django.conf import settings
import jwt


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
        "employee_approve": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "active": [["admin"], ["super_admin"]],
        "de_active": [["admin"], ["super_admin"]],
    }
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return UserRegisterSerializer
        if self.action in ("active", "de_active"):
            return None
        if self.action in ("forgot_password"):
            return ForgotPasswordSerializer
        if self.action in ("change_password"):
            return ChangePasswordSerializer
        if self.action in ("token"):
            return TokenSerializer
        if self.action in ("rest_password"):
            return PasswordSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ("forgot_password", "token", "rest_password"):
            self.permission_classes = []
        else:
            self.permission_classes = [TokenHasActionScope]
        return super(self.__class__, self).get_permissions()

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

    @action(detail=False, methods=["post"])
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=request.data.get("email")).first()
        if user:
            token = jwt.encode({'user_id': str(user.id)}, settings.SECRET_KEY, algorithm='HS256')
            site = settings.HOST_URL
            url = site + "/" + "reset_password" + "?token=" + str(token)
            body = "Link rest password : " + url
            mail_data = {
                "template": "mail_templates/mail_successful_file_registration.html",
                "subject": "Đăng ký hồ sơ thành công",
                "context": {
                    "name": user.name,
                    "body": body,
                    "title": "Dịch vụ công Epoch Making xin thông báo"
                },
                "to": [request.data.get("email")],
            }
            SendMail.send_html_email(mail_data)
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response("Không tìm thấy email", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False)
    def token(self, request):
        token = request.data.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                return Response({'msg': 'Tài khoản đã bị khóa'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg': 'Xác thực email thành công'}, status=status.HTTP_202_ACCEPTED)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False)
    def rest_password(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                return Response({'msg': 'Tài khoản đã bị khóa'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()
            return Response({'msg': 'Reset mật khẩu thành công'}, status=status.HTTP_202_ACCEPTED)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False)
    def employee_approve(self, request):
        query = User.objects.filter(roles__scope="employee_approve")
        serializer = UserSerializer(query, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def employee_receive(self, request):
        query = User.objects.filter(roles__scope="employee_receive")
        serializer = UserSerializer(query, many=True)
        return Response(serializer.data)
