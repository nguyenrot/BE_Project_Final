from api_base.models import TimeStampedModel
from django.db import models
from api_files.models import ReceptionRecord
from api_users.models import User
import uuid


class ApproveRecord(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    reception_record = models.ForeignKey(ReceptionRecord, on_delete=models.CASCADE, blank=False, null=False,
                                         related_name="approve")
    user_assignment = models.ForeignKey(User, related_name="approve_record", on_delete=models.CASCADE, blank=False,
                                        null=False)
    start_day = models.DateField(blank=False, null=False)
    end_day = models.DateField(blank=False, null=False)
