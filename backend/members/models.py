# Django imports 
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


def upload_to(instance, filename):
    return 'members_profile/{filename}'.format(filename = filename)

class Member(models.Model):
    first_name = models.CharField(max_length = 256, unique = False, db_index = True)
    mid_name = models.CharField(max_length = 256, db_index = True)
    last_name = models.CharField(max_length = 256, db_index = True)
    mother_name = models.CharField(max_length = 256, db_index = True)
    gender = models.CharField(max_length = 16, choices = User.GenderType.choices, default = User.GenderType.MALE)
    phone = models.CharField(max_length = 16, unique = False, null = False) #!Unique must be set to True
    current_city =  models.CharField(max_length = 65, blank=True, null=True)
    work = models.CharField(max_length = 128)
    martial_status = models.CharField(max_length = 32, choices = User.MartialStatus.choices)
    email = models.EmailField(_("email address"), unique=True, db_index = True)
    age = models.IntegerField(default = 15)
    date_joined = models.DateTimeField(auto_now_add = True)
    social_media_profiles = models.JSONField()
    is_active = models.BooleanField(default = True)
    profile_image = models.ImageField(_("Images"), upload_to = upload_to, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Member"