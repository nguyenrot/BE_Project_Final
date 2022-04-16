from django.db import models
from api_services.models import Service
from api_base.models import TimeStampedModel
import uuid


class File(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=255, blank=False, null=False)
    service = models.ForeignKey(Service, related_name="files", blank=False, null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = "files"