# Generated by Django 4.2.6 on 2024-01-13 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(db_index=True, max_length=256)),
                ('mid_name', models.CharField(db_index=True, max_length=256)),
                ('last_name', models.CharField(db_index=True, max_length=256)),
                ('mother_name', models.CharField(db_index=True, max_length=256)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], default='MALE', max_length=16)),
                ('phone', models.CharField(max_length=16)),
                ('user_type', models.CharField(choices=[('PARTICIPANT', 'Participant'), ('MEMBER', 'Member'), ('ADMIN', 'Admin')], default='PARTICIPANT', max_length=16)),
                ('current_city', models.CharField(blank=True, max_length=65, null=True)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='email address')),
                ('age', models.IntegerField(default=15)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('otp', models.CharField(blank=True, max_length=200, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Users',
                'verbose_name_plural': 'Users Data',
            },
        ),
    ]
