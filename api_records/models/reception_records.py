from django.db import models
from api_fields.models import Field
from api_services.models import Service
import uuid


class ReceptionRecords(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    sender_name = models.CharField(max_length=255, null=False, blank=False)
    sent_date = models.DateTimeField(auto_now_add=True)
    # field = models.ForeignKey(Field, on_delete=models.CASCADE, blank=False, null=False, related_name="records")
    name = models.CharField(max_length=255, blank=False, null=False)
    records = models.JSONField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=False, null=False, related_name="records")
    address = models.TextField(null=False, blank=False)
    phone_number = models.CharField(max_length=11, null=False, blank=False)
    status = models.CharField(max_length=255, default="Đang tiếp nhận")
    approve = models.BooleanField(default=False)
    assignment = models.BooleanField(default=False)

    class Meta:
        db_table = "reception_records"
