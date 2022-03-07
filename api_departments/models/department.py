from django.db import models
import uuid
from django.template.defaultfilters import slugify


class Department(models.Model):
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
