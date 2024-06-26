# Generated by Django 4.1.13 on 2024-06-03 12:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0010_alter_activity_activity_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservations', '0003_alter_reservation_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reservation',
            new_name='Request',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='reservation_created_at',
            new_name='request_created_at',
        ),
    ]
