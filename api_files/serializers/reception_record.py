from rest_framework import serializers
from api_files.models import ReceptionRecord, ReceptionRecordDetail, ApproveRecord


class ReceptionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptionRecord
        fields = ["id", "name_sender", "phone_number", "address", "email", "file", "code"]


class ReceptionRecordDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptionRecordDetail
        fields = "__all__"
        extra_fields = ["ingredient", "original", "copy", "note", "status", "form", "file"]


class ViewCustomerRecordSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    details = ReceptionRecordDetailSerializer(many=True, read_only=True)
    file = serializers.SerializerMethodField()

    def get_file(self, instance):
        return instance.file.name

    class Meta:
        model = ReceptionRecord
        fields = ["id", "name_sender", "code", "phone_number", "address", "email", "file", "status", "details",
                  "status_display"]
