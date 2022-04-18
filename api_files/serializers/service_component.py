from rest_framework import serializers
from api_files.models import ServiceComponent


class ServiceComponentSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServiceComponent
        fields = "__all__"
