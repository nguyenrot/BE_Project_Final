# Generated by Django 4.0.3 on 2022-04-18 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_files', '0002_remove_servicecomponent_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicecomponent',
            name='form',
        ),
        migrations.AlterField(
            model_name='servicecomponent',
            name='file_sample',
            field=models.FileField(blank=True, default=True, null=True, upload_to=''),
        ),
    ]
