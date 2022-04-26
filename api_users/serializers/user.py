from rest_framework import serializers
from api_users.models import User
from django.contrib.auth.hashers import make_password


def get_list_name_roles(list_role):
    roles = []
    for role in list_role:
        roles.append(role.name)
    return roles


class UserSerializer(serializers.ModelSerializer):
    # roles = serializers.SerializerMethodField()
    #
    # def get_roles(self, user):
    #     return user.roles.first().name

    list_role = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)

    def get_list_role(self, user):
        return get_list_name_roles(user.roles.all())

    class Meta:
        model = User
        fields = ["id", "name", "email", "phone", "birthday", "address", "place", "avatar", "department", "position",
                  "roles", "list_role", "is_active",
                                        "username", "created_at", "updated_at"]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "phone", "birthday", "address", "place", "avatar", "department", "position", "roles",
                  "username", "password", "created_at", "updated_at"]

    def create(self, validated_data):
        roles = validated_data.pop("roles")
        user = User.objects.create(**validated_data)
        user.password = make_password(user.password)
        user.roles.add(roles[0])
        user.save()
        return user
