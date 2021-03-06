from django.db import models
from api_fields.models import Field
from api_base.models import TimeStampedModel
import uuid


class Service(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=255, blank=False, null=False)
    decision_number = models.CharField(max_length=255, blank=False, null=False)
    type_procedure = models.CharField(max_length=255, blank=True, null=True)
    field = models.ForeignKey(Field, related_name="services", blank=False, null=False, on_delete=models.CASCADE)
    code_DVCQG = models.CharField(max_length=255, blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)
    method = models.JSONField(blank=True, null=True)
    amount = models.IntegerField(default=None, null=True, blank=True)
    object = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    receiving_address = models.CharField(max_length=255, blank=True, null=True)
    juridical = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "service"
