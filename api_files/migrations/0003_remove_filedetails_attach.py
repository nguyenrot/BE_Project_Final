# Generated by Django 4.0.3 on 2022-04-16 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_files', '0002_alter_filedetails_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filedetails',
            name='attach',
        ),
    ]