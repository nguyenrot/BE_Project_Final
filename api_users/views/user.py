from email import message
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from uritemplate import partial
from api_base.views import BaseViewSet
from api_users.models import User
from api_users.serializers import (
    UserSerializer,
    UpdateProfileSerializer,
    ChangePasswordSerializer,
    ActivateSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from api_users.services import UserService
from rest_framework.decorators import action
from rest_framework import status


class UserView(BaseViewSet):
    queryset = User.objects.all()
    required_alternate_scopes = {
        "list": [["user:access_personal"]],
        "retrieve": [["user:access_personal"]],
        "change_password": [["user:access_personal"]],
        "update": [["admin:edit_user"]],
        "destroy": [["admin:delete_user"]],
        "activate": [["admin:activate_user"]],
        "deactivate": [["admin:invite_user"]],
        "get_profile": [["user:access_personal"]],
        "update_profile": [["user:access_personal"]],
    }

    def get_serializer_class(self):
        if self.action == "change_password":
            return ChangePasswordSerializer
        if self.action in ["activate", "deactivate"]:
            return ActivateSerializer
        if self.action in ["retrieve", "update"]:
            return UserSerializer
        elif self.action == "forgot_password":
            return ForgotPasswordSerializer
        elif self.action == "reset_password":
            return ResetPasswordSerializer
        return UpdateProfileSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if UserService.check_password(request.user, request.data.get("password")):
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(
            {"error": ["wrong password"]}, status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=False, methods=["PATCH"], url_path="change-password")
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

    @action(detail=False, methods=["GET"], url_path="password-created")
    def password_created(self, request):
        return Response(
            {"created": request.user.has_usable_password()}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["GET"], url_path="mine")
    def get_profile(self, request):
        user = User.objects.filter(pk=request.user.id).first()
        serializer = UpdateProfileSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=["PUT"])
    def update_profile(self, request):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(methods=["PUT"], detail=True)
    def activate(self, request, *args, **kwargs):
        user = self.get_object()
        UserService.activate_user(user)
        return Response({"Success": True})

    @action(methods=["PUT"], detail=True)
    def deactivate(self, request, *args, **kwargs):
        user = self.get_object()
        UserService.deactivate_user(user)
        return Response({"Success": True})

    @action(
        detail=False,
        methods=["POST"],
        url_path="forgot-password",
        permission_classes=[],
    )
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_password_uri = request.build_absolute_uri("/reset-password")
        email = serializer.data.get("email")
        message = UserService.forgot_password(email, reset_password_uri)
        status_code = {
            "success": status.HTTP_200_OK,
            "fail": status.HTTP_400_BAD_REQUEST,
            "[error] email invalid": status.HTTP_406_NOT_ACCEPTABLE,
        }
        return Response({"msg": message}, status=status_code.get(message))

    @action(
        detail=True, methods=["PATCH"], url_path="reset-password", permission_classes=[]
    )
    def reset_password(self, request, pk=None):
        user = User.objects.filter(pk=pk).first()
        serializer = ResetPasswordSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.save():
            message, status_code = "success", status.HTTP_200_OK
        else:
            message, status_code = "fail", status.HTTP_400_BAD_REQUEST
        return Response({"msg": message}, status=status_code)
