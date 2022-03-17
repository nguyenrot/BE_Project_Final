from rest_framework import serializers
from api_records.models import ReceptionRecords


class ReceptionRecordsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReceptionRecords
        fields = "__all__"
