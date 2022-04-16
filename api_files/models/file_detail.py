from django.db import models
from api_base.models import TimeStampedModel
from api_files.models import File
import uuid


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class FileDetails(TimeStampedModel):
    STATUS_CHOICES = [
        (1, "Xuất trình"),
        (2, "Giao nộp")
    ]

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    ingredient = models.TextField(blank=False, null=False)
    attach = models.FileField(blank=False, null=False)
    original = models.IntegerField(default=0)
    copy = models.IntegerField(default=0)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default=2, max_length=1)
    form = models.TextField(blank=True, null=True)
    file = models.ForeignKey(File, blank=False, null=False, on_delete=models.CASCADE, related_name="details")

    class Meta:
        db_table = "files_details"
