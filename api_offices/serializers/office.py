from rest_framework import serializers
from api_offices.models import Office, Group


class OfficeSerializer(serializers.ModelSerializer):
    name_parent_office = serializers.SerializerMethodField()
    name_group = serializers.SerializerMethodField()

    def get_name_parent_office(self, instance):
        return instance.parent_office.name if instance.parent_office else None

    def get_name_group(self, instance):
        return instance.group.name if instance.group else "các đơn vị cấp xã trực thuộc huyện"

    class Meta:
        model = Office
        fields = "__all__"
        extra_fields = ["name_parent_office", "name_group"]
