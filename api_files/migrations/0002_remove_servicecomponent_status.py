# Generated by Django 4.0.3 on 2022-04-18 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_files', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicecomponent',
            name='status',
        ),
    ]
