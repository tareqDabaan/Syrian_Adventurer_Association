# Django imports 
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models

# Django imports
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    
    #? Custom user model manager where email is the unique identifiers for authentication instead of usernames.

    def create_user(self, email, password, **extra_fields):
        #? Create and save a user with the given email and password.

        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(
            email = email
            , password = make_password(password) 
            ,**extra_fields)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        #? Create and save a SuperUser with the given email and password.
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields["user_type"] = User.ADMIN_TYPE
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff = True."))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser = True."))
        return self.create_user(email, password, **extra_fields)
    
  
def upload_to(instance, filename):
    return f'members_profile_picture/{instance.email}/{filename}'


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
    profile_image = models.ImageField(_("Images"), upload_to = upload_to, blank=True, null=True)
    mother_name = models.CharField(max_length = 256, db_index = True)
    gender = models.CharField(max_length = 16, choices = GenderType.choices, default = GenderType.MALE)
    phone = models.CharField(max_length = 16, unique = False, null = False) #!Unique must be set to True
    base_type = UserType.PARTICIPANT
    ADMIN_TYPE = UserType.ADMIN
    user_type = models.CharField(max_length = 16, choices = UserType.choices, default = base_type )
    current_city =  models.CharField(max_length = 16, unique = False, null = False) #! PointField 
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
    otp_sent_time = models.DateTimeField(blank=True, null=True)

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
    