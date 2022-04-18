from api_base.models import TimeStampedModel
from django.db import models
from api_files.models import ReceptionRecord
from api_files.models import ServiceComponent
import uuid


class ReceptionRecordDetail(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    reception_record = models.ForeignKey(ReceptionRecord, on_delete=models.CASCADE, null=False, blank=False,
                                         related_name="details")
    attach = models.FileField(blank=False, null=False)
    service_component = models.ForeignKey(ServiceComponent, on_delete=models.CASCADE, null=False, blank=False,
                                          related_name="record_detail")
