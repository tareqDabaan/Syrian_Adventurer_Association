# Django imports 
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from typing import Any

# Local modules imports
from users.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    
    class GenderType(models.TextChoices):
        MALE = ("MALE", "Male")
        FEMALE = ("FEMALE", "Female")

    class UserType(models.TextChoices):
        PARTICIPANT = ("PARTICIPANT", "Participant")
        MEMBER = ("MEMBER", "Member")
        ADMIN = ("ADMIN", "Admin")
    
    class MartialStatus(models.TextChoices):
        SINGLE = ("SINGLE", "Single")
        MARRIED = ("MARRIED", "Married")
        WIDOWED = ("WIDOWED", "Widowed")
        DIVORCED = ("DIVORCED", "Divorced")
        SEPARATED = ("SEPARATED", "Separated")

    first_name = models.CharField(max_length = 256, unique = False, db_index = True)
    mid_name = models.CharField(max_length = 256, db_index = True)
    last_name = models.CharField(max_length = 256, db_index = True)
    mother_name = models.CharField(max_length = 256, db_index = True)
    gender = models.CharField(max_length = 16, choices = GenderType.choices, default = GenderType.MALE)
    phone = models.CharField(max_length = 16, unique = False, null = False) #!Unique must be set to True
    base_type = UserType.PARTICIPANT
    user_type = models.CharField(max_length = 16, choices = UserType.choices, default = base_type )
    # profile_image = models.ImageField()
    current_city =  models.CharField(max_length = 65, blank=True, null=True)
    emergency_number = models.CharField(max_length = 16, unique = False, null = False) #!Unique must be set to True
    work = models.CharField(max_length = 32)
    martial_status = models.CharField(max_length = 32, choices = MartialStatus.choices)
    discount = models.BooleanField(default = False)
    email = models.EmailField(_("email address"), unique=True, db_index = True)
    age = models.IntegerField(default = 15)
    is_verified = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    otp = models.CharField(max_length = 200, null = True, blank = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"
        
    def __str__(self):
        return self.email


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    can_update_password = models.BooleanField(default = False)
    
    def __str__(self) -> str:
        return self.user.email
    

class Member(models.Model):
    first_name = models.CharField(max_length = 256, unique = False, db_index = True)
    mid_name = models.CharField(max_length = 256, db_index = True)
    last_name = models.CharField(max_length = 256, db_index = True)
    mother_name = models.CharField(max_length = 256, db_index = True)
    gender = models.CharField(max_length = 16, choices = User.GenderType.choices, default = User.GenderType.MALE)
    phone = models.CharField(max_length = 16, unique = False, null = False) #!Unique must be set to True
    current_city =  models.CharField(max_length = 65, blank=True, null=True)
    work = models.CharField(max_length = 32)
    martial_status = models.CharField(max_length = 32, choices = User.MartialStatus.choices)
    email = models.EmailField(_("email address"), unique=True, db_index = True)
    age = models.IntegerField(default = 15)
    date_joined = models.DateTimeField(auto_now_add = True)
    social_media_profiles = models.JSONField()
    # profile_image = models.ImageField()

    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Member"
