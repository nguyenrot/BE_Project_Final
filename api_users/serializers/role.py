from rest_framework import serializers
from api_users.models import Role


class RoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
