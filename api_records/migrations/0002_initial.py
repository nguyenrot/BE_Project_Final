# Generated by Django 4.0.3 on 2022-03-27 01:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_records', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='approverecords',
            name='user_approve',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approve_records', to=settings.AUTH_USER_MODEL),
        ),
    ]