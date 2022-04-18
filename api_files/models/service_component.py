from django.db import models
from api_base.models import TimeStampedModel
from api_services.models import Service
import uuid


class ServiceComponent(TimeStampedModel):
    STATUS_CHOICES = [
        (1, "Xuất trình"),
        (2, "Giao nộp")
    ]

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    ingredient = models.TextField(blank=False, null=False)
    original = models.IntegerField(default=0)
    copy = models.IntegerField(default=0)
    note = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=2)
    form = models.TextField(blank=True, null=True)
    file_sample = models.FileField(blank=False, null=False)
    service = models.ForeignKey(Service, blank=False, null=False, on_delete=models.CASCADE, related_name="components")

    class Meta:
        db_table = "files_details"
