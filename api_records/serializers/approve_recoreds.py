from rest_framework import serializers
from api_records.models import ApproveRecords


class ApproveRecordsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApproveRecords
        fields = "__all__"
