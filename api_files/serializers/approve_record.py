from rest_framework import serializers
from api_files.models import ReceptionRecord, ReceptionRecordDetail, ApproveRecord


class ApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApproveRecord
        fields = "__all__"


class ContentSerializer(serializers.Serializer):
    content = serializers.CharField(default=None)
