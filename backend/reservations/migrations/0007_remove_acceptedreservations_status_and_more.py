# Generated by Django 4.1.13 on 2024-06-03 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0010_alter_activity_activity_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservations', '0006_acceptedreservations_delete_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acceptedreservations',
            name='status',
        ),
        migrations.CreateModel(
            name='RejectedReservations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rejected_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('reason', models.TextField()),
                ('activity_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activities.activity')),
                ('participant_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
