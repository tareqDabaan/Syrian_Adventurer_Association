# Generated by Django 4.1.13 on 2024-06-10 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messages',
            options={'verbose_name': 'Messages', 'verbose_name_plural': 'Messages'},
        ),
        migrations.AddField(
            model_name='messages',
            name='sent_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
