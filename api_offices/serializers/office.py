from rest_framework import serializers
from api_offices.models import Office, Group


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"
