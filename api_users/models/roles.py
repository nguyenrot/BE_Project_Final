from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(default="", blank=True)
    scope = models.TextField(default="", blank=True)
    last_modified_by = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ac_roles"
