from django.db import models
from api_base.models import TimeStampedModel
import uuid


class News(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)

    class Meta:
        db_table = "news"
