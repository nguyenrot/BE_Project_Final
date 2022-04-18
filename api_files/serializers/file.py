from rest_framework import serializers
from api_files.serializers.file_details import FileDetailsSerializer


# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         fields = "__all__"
#
#
# class GetFileSerializer(serializers.ModelSerializer):
#     details = FileDetailsSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = File
#         fields = "__all__"
#         extra_fields = ["details"]
