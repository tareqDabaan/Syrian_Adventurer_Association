# Generated by Django 4.1.13 on 2024-07-05 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0003_messages_is_spam'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]