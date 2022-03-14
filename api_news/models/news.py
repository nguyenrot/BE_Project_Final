from django.db import models
import uuid


class News(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)

    class Meta:
        db_table = "news"
