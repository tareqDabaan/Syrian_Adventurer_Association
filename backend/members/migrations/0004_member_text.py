# Generated by Django 4.1.13 on 2024-06-13 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_member_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]