from rest_framework import serializers
from api_services.models import Service
from api_files.models import ServiceComponent


class ServiceComponentSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServiceComponent
        fields = "__all__"


class ServiceSerializers(serializers.ModelSerializer):
    field_name = serializers.SerializerMethodField()
    office_name = serializers.SerializerMethodField()
    components = ServiceComponentSerializers(many=True, read_only=True)

    def get_field_name(self, service):
        return service.field.name

    def get_office_name(self, service):
        return service.field.office.name

    class Meta:
        model = Service
        fields = "__all__"
        extra_fields = ["field_name", "office_name", "components"]


class ServiceListSerializers(serializers.ModelSerializer):
    field_name = serializers.SerializerMethodField()

    def get_field_name(self, service):
        return service.field.name

    class Meta:
        model = Service
        fields = ["id", "name", "field_name", "amount"]
