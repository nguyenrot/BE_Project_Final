from django.db import models
from api_fields.models import Field


class Service(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    field = models.ForeignKey(Field, related_name="services", blank=False, null=False, on_delete=models.CASCADE)
    description = models.TextField(blank=False, null=False)

    class Meta:
        db_table = "service"
