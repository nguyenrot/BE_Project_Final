# Generated by Django 4.0.3 on 2022-04-30 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_users', '0007_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/%Y/%m/%d/%H/%M/%s/'),
        ),
    ]
