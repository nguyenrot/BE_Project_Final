from rest_framework import serializers
from api_users.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    def get_roles(self, user):
        return user.roles.first().name

    class Meta:
        model = User
        fields = ["id", "name", "email", "phone", "birthday", "address", "place", "avatar", "department", "position",
                  "roles",
                  "username"]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "phone", "birthday", "address", "place", "avatar", "department", "position", "roles",
                  "username", "password"]

    def create(self, validated_data):
        roles = validated_data.pop("roles")
        user = User.objects.create(**validated_data)
        user.password = make_password(user.password)
        user.roles.add(roles[0])
        user.save()
        return user
