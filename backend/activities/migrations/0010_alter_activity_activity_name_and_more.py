# Generated by Django 4.2.6 on 2024-05-17 14:51

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0009_activity_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='activity',
            name='destination_location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326),
        ),
        migrations.AlterField(
            model_name='activity',
            name='location',
            field=models.CharField(max_length=56),
        ),
        migrations.AlterField(
            model_name='activity',
            name='starting_point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326),
        ),
    ]
