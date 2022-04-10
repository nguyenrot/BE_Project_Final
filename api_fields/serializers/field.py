from rest_framework import serializers
from api_fields.models import Field


class FieldSerializers(serializers.ModelSerializer):
    name_parent_office = serializers.SerializerMethodField()

    def get_name_parent_office(self, instance):
        return instance.parent_office.name if instance.parent_office else None

    class Meta:
        model = Field
        fields = "__all__"
        extra_fields = ["name_parent_office"]
