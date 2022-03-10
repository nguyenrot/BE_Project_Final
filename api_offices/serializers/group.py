from rest_framework import serializers
from api_offices.models import Office, Group
from api_offices.serializers import OfficeSerializer
from api_offices.services import OfficeService


class GroupListSerializer(serializers.ModelSerializer):
    office_childs = serializers.SerializerMethodField()

    def get_office_childs(self, group):
        return OfficeService.get_tree(group)

    class Meta:
        model = Group
        fields = ["id", "name", "office_childs"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]
