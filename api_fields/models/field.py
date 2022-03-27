from django.db import models
from api_base.models import TimeStampedModel
from api_offices.models import Office


class Field(TimeStampedModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    office = models.ForeignKey(Office, related_name="fields", blank=False, null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = "field"
