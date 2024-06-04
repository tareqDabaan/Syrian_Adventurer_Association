# Generated by Django 4.1.13 on 2024-06-03 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_rename_reservation_request_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('request_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reservations.request')),
                ('approve', models.CharField(blank=True, max_length=200, null=True)),
            ],
            bases=('reservations.request',),
        ),
    ]
