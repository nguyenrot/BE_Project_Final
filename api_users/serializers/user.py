from rest_framework.serializers import ModelSerializer

from api_users.models import User
from rest_framework import serializers, fields
from api_users.models import User
from utils.utils import Util
from api_users.services import UserService


class UserRoleSerializer(serializers.Serializer):
    id = fields.IntegerField(label="ID")
    name = fields.CharField(max_length=200, read_only=True)


class UserSerializer(ModelSerializer):
    roles = UserRoleSerializer(many=True, required=False)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "last_name",
            "first_name",
            "email",
            "roles",
            "password",
        ]

    def update(self, instance, validated_data):
        validated_data.pop("password")
        validated_data.pop("username")
        if instance.email != validated_data.get("email"):
            Invite.objects.filter(email=instance.email).update(
                email=validated_data.get("email")
            )
            LinkingAccount.objects.filter(user=instance).delete()
        return UserService.update(instance, validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("password")
        return ret


class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(allow_blank=True)
    newPassword = serializers.CharField(required=True)


class ActivateSerializer(serializers.Serializer):
    id = serializers.UUIDField(format="hex")


class UpdateProfileSerializer(ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["id", "username", "last_name",
                  "first_name", "email", "password"]

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("username")
        if instance.check_password(password):
            Invite.objects.filter(email=instance.email).update(
                email=validated_data.get("email")
            )
            LinkingAccount.objects.filter(user=instance).delete()
            instance = super().update(instance, validated_data)
            return instance
        raise serializers.ValidationError({"error": ["wrong password"]})

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("password")
        return ret


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        token = attrs.get("token")
        status = Util.HS256_decode(token)
        if status in ["token expired", "token invalid"]:
            raise serializers.ValidationError(
                {"msg": "[error] token invalid or expired"}
            )

        return attrs

    def update(self, instance, validated_data):
        token = validated_data.get("token")
        password = validated_data.get("password")
        id = Util.HS256_decode(token).get("id", None)
        if str(instance.id) != id:
            raise serializers.ValidationError(
                {"msg": "[error] can't edit this user"})

        instance.set_password(password)
        instance.save()
        return instance
