from django.db import models
from api_offices.models import Group
import uuid


class Office(models.Model):
    nanme = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    parent_office = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="offices", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "offices"
