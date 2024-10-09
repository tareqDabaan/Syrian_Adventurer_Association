# Generated by Django 4.1.13 on 2024-08-14 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_price_min', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('preferred_price_max', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('preferred_month', models.CharField(blank=True, max_length=20, null=True)),
                ('preferred_places', models.CharField(blank=True, max_length=256, null=True)),
                ('preferred_types', models.CharField(blank=True, max_length=256, null=True)),
                ('preferred_difficulity', models.CharField(blank=True, max_length=256, null=True)),
                ('more_than_day', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'verbose_name': 'User Preference',
                'verbose_name_plural': 'User Preferences',
            },
        ),
    ]
