# Generated by Django 4.2.6 on 2024-03-24 02:33

import activities.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_alter_activitytype_activity_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitytype',
            options={'verbose_name': 'Activity Type', 'verbose_name_plural': 'Activity Type'},
        ),
        migrations.AlterField(
            model_name='activity',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=activities.models.upload_to, verbose_name='Images'),
        ),
        migrations.AlterField(
            model_name='activitytype',
            name='tent_price',
            field=models.DecimalField(decimal_places=3, default=50.0, max_digits=10),
        ),
    ]