from django.db import models
from api_records.models import ReceptionRecords


class Evaluate(models.Model):
    record = models.ForeignKey(ReceptionRecords, on_delete=models.SET_NULL, related_name="evaluate", null=True,
                               blank=True)
    evaluate = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "evaluate"
