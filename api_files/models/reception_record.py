from api_base.models import TimeStampedModel
from django.db import models
from api_files.models import File
import uuid


class ReceptionRecord(TimeStampedModel):
    STATUS_CHOICES = [
        (0, "Chờ thanh toán"),
        (1, "Đã gửi, đang tiếp nhận"),
        (2, "Đã tiếp nhận, đang duyệt"),
        (3, "Đã duyệt"),
        (4, "Đã hủy")
    ]
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name_sender = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(default=None, max_length=10, null=True)
    sent_date = models.DateTimeField(auto_now_add=True)
    file = models.ForeignKey(File, related_name="reception", null=False, blank=False, on_delete=models.CASCADE)
    address = models.TextField(blank=False, null=False)
    phone_number = models.CharField(blank=False, null=False, max_length=10)
    email = models.EmailField(blank=False, null=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    payment = models.BooleanField(default=False)
    order_id = models.CharField(max_length=255, default=None, null=True, blank=True)
    request_id = models.CharField(max_length=255, default=None, null=True, blank=True)
    link_payment = models.TextField(default=None, null=True, blank=True)
    assignment = models.BooleanField(default=False)
    content = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
