# Generated by Django 4.2.6 on 2024-01-22 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(db_index=True, max_length=256)),
                ('mid_name', models.CharField(db_index=True, max_length=256)),
                ('last_name', models.CharField(db_index=True, max_length=256)),
                ('mother_name', models.CharField(db_index=True, max_length=256)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], default='MALE', max_length=16)),
                ('phone', models.CharField(max_length=16)),
                ('current_city', models.CharField(blank=True, max_length=65, null=True)),
                ('work', models.CharField(max_length=32)),
                ('martial_status', models.CharField(choices=[('SINGLE', 'Single'), ('MARRIED', 'Married'), ('WIDOWED', 'Widowed'), ('DIVORCED', 'Divorced'), ('SEPARATED', 'Separated')], max_length=32)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='email address')),
                ('age', models.IntegerField(default=15)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('social_media_profiles', models.JSONField()),
            ],
            options={
                'verbose_name': 'Member',
                'verbose_name_plural': 'Member',
            },
        ),
    ]
