from django.db import models
from api_base.models import TimeStampedModel
import uuid
from django.template.defaultfilters import slugify


class Department(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    discription = models.TextField(max_length=255, blank=True, null=True)

    def get_slug(self):
        return slugify(self.name)

    class Meta:
        db_table = "department"
