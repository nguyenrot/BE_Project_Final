from django.db import models
from api_base.models import TimeStampedModel
from api_services.models import Service
import uuid


class ServiceComponent(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    ingredient = models.TextField(blank=False, null=False)
    original = models.IntegerField(default=0)
    copy = models.IntegerField(default=0)
    note = models.TextField(blank=True, null=True)
    file_sample = models.FileField(blank=True, null=True, default=True)
    service = models.ForeignKey(Service, blank=False, null=False, on_delete=models.CASCADE, related_name="components")

    class Meta:
        db_table = "files_details"
