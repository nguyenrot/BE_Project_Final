from rest_framework import serializers
from api_files.models import FileDetails


class FileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileDetails
        fields = "__all__"
