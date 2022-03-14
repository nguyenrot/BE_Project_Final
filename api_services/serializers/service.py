from rest_framework import serializers
from api_services.models import Service


class ServiceSerializers(serializers.ModelSerializer):
    field_name = serializers.SerializerMethodField()

    def get_field_name(self, service):
        return service.field.name

    class Meta:
        model = Service
        fields = ["id", "field", "name", "description", "field_name"]
