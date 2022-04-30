# Generated by Django 4.0.3 on 2022-04-30 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_files', '0004_alter_receptionrecorddetail_attach_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receptionrecorddetail',
            name='attach',
            field=models.FileField(upload_to='records/%Y/%m/%d/%H/%i/%s/'),
        ),
        migrations.AlterField(
            model_name='servicecomponent',
            name='file_sample',
            field=models.FileField(blank=True, default=True, null=True, upload_to='samples/%Y/%m/%d/%H/%i/%s/'),
        ),
    ]
