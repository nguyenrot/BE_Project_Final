from api_base.models import TimeStampedModel
from api_files.models import ReceptionRecord
from django.db import models
import uuid


class Evaluate(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    record = models.ForeignKey(ReceptionRecord, on_delete=models.CASCADE, null=False, blank=False,
                               related_name="evaluate")
    question_1 = models.IntegerField(null=False, blank=False)
    question_2 = models.IntegerField(null=False, blank=False)
    question_3 = models.IntegerField(null=False, blank=False)
    question_4 = models.IntegerField(null=False, blank=False)
    question_5 = models.IntegerField(null=False, blank=False)
