from rest_framework import serializers
from api_files.models import ReceptionRecord, ReceptionRecordDetail, ApproveRecord


class ReceptionRecordSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    service = serializers.SerializerMethodField()

    def get_service(self, instance):
        return instance.service.name

    class Meta:
        model = ReceptionRecord
        fields = ["id", "name_sender", "phone_number", "address", "email", "service", "code", "status",
                  "status_display"]


class ReceptionRecordDetailSerializer(serializers.ModelSerializer):
    ingredient = serializers.SerializerMethodField()
    original = serializers.SerializerMethodField()
    copy = serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()

    def get_ingredient(self, instance):
        return instance.service_component.ingredient

    def get_original(self, instance):
        return instance.service_component.original

    def get_copy(self, instance):
        return instance.service_component.copy

    def get_note(self, instance):
        return instance.service_component.note

    class Meta:
        model = ReceptionRecordDetail
        fields = "__all__"
        extra_fields = ["ingredient", "original", "copy", "note"]


class ViewCustomerRecordSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    details = ReceptionRecordDetailSerializer(many=True, read_only=True)
    service = serializers.SerializerMethodField()
    pay_url = serializers.SerializerMethodField()

    def get_pay_url(self, instance):
        return instance.payment.pay_url

    def get_service(self, instance):
        return instance.service.name

    class Meta:
        model = ReceptionRecord
        fields = ["id", "name_sender", "code", "phone_number", "address", "email", "service", "status", "details",
                  "status_display", "pay_url"]
