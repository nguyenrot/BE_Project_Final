from django.db import models
from api_users.models import User
from api_records.models import ReceptionRecords
import uuid


class ApproveRecords(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    reception_records = models.ForeignKey(ReceptionRecords, related_name="approve_records", null=False, blank=False,
                                          on_delete=models.CASCADE)
    user_approve = models.ForeignKey(User, related_name="approve_records", null=False, blank=False,
                                     on_delete=models.CASCADE)
    start_day = models.DateField(auto_now_add=True)
    last_day = models.DateField(null=False, blank=False)
    status = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "approve_records"
