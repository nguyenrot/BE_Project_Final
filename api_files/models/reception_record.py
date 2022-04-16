from api_base.models import TimeStampedModel
from django.db import models
from api_files.models import File
import uuid


class ReceptionRecord(TimeStampedModel):
    STATUS_CHOICES = [
        (1, "Đã gửi, đang tiếp nhận"),
        (2, "Đã tiếp nhận, đang duyệt"),
        (3, "Đã duyệt"),
        (4, "Đã hủy")
    ]
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name_sender = models.CharField(max_length=255, null=False, blank=False)
    sent_date = models.DateTimeField(auto_now_add=True)
    file = models.ForeignKey(File, related_name="reception", null=False, blank=False, on_delete=models.CASCADE)
    address = models.TextField(blank=False, null=False)
    phone_number = models.CharField(blank=False, null=False, max_length=10)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    assignment = models.BooleanField(default=False)
    content = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
