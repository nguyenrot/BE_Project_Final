from rest_framework import serializers
from api_records.models import ApproveRecords
from django.db.models import F


class ApproveRecordsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApproveRecords
        fields = "__all__"

    def create(self, validated_data):
        reception_records = validated_data.get("reception_records")
        reception_records.assignment = True
        reception_records.save()
        return super().create(validated_data)
