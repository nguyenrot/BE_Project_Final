# Generated by Django 4.0.3 on 2022-03-06 07:14

from django.db import migrations


def add_role(apps, schema_editor):
    Role = apps.get_model("api_users", "Role")

    Role.objects.get_or_create(
        name="Employee receive",
        description="Account employe receive",
        scope="employee_receive",
    )
    Role.objects.get_or_create(
        name="Employee approve",
        description="Account employe approve",
        scope="employee_approve",
    )


class Migration(migrations.Migration):
    dependencies = [
        ('api_users', '0002_auto_20220305_1556'),
    ]

    operations = [migrations.RunPython(add_role, migrations.RunPython.noop)]
