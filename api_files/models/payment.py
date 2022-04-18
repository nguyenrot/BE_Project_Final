from api_base.models import TimeStampedModel
from django.db import models
import uuid


class Payment(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    order_id = models.CharField(max_length=255, default=None, null=True, blank=True)
    request_id = models.CharField(max_length=255, default=None, null=True, blank=True)
    pay_url = models.TextField(default=None, null=True, blank=True)
    response_time = models.IntegerField(default=None, null=True, blank=True)
    message = models.TextField(default=None, null=True, blank=True)
    result_code = models.CharField(max_length=255, null=True, blank=True)
    deep_link = models.TextField(default=None, null=True, blank=True)
    qr_code_url = models.TextField(default=None, null=True, blank=True)
