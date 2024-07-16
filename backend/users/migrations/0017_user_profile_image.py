# Generated by Django 4.1.13 on 2024-04-06 19:34

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.upload_to, verbose_name='Images'),
        ),
    ]