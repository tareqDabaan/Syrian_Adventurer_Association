# Generated by Django 4.2.6 on 2024-03-24 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_member_profile_image'),
        ('activities', '0008_remove_activity_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='members',
            field=models.ManyToManyField(to='members.member'),
        ),
    ]
