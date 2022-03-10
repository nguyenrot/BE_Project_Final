from rest_framework import serializers
from api_fields.models import Field


class FieldSerializers(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"
