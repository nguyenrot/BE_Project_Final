# Generated by Django 4.0.3 on 2022-04-16 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_files', '0003_remove_filedetails_attach'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedetails',
            name='status',
            field=models.IntegerField(choices=[(1, 'Xuất trình'), (2, 'Giao nộp')], default=2),
        ),
        migrations.CreateModel(
            name='ReceptionRecord',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name_sender', models.CharField(max_length=255)),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=10)),
                ('status', models.IntegerField(choices=[(1, 'Đã gửi, đang tiếp nhận'), (2, 'Đã tiếp nhận, đang duyệt'), (3, 'Đã duyệt'), (4, 'Đã hủy')], default=1)),
                ('assignment', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reception', to=settings.AUTH_USER_MODEL)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reception', to='api_files.file')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
