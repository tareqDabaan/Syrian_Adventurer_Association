# Django imports 
from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models as gismodels

# Local modules imports
from users.models import User 
from members.models import Member

def upload_to(instance, filename):
    return 'activities/{filename}'.format(filename = filename)
    
    
class ActivityType(models.Model):
    
    class Type(models.TextChoices):
        CAMPING = ("CAMPING", "Camping")
        HICKING = ("HICKING", "Hicking")
        
    include_tent = models.BooleanField(default = False,)
    tent_price = models.DecimalField(max_digits = 10, decimal_places = 3, default = 50.000)
    difficulity_level = models.CharField(max_length = 56, blank=True, null=True)
    activity_type = models.CharField(max_length = 56, choices = Type.choices, blank=True, null=True)
    
    class Meta:
        verbose_name = "Activity Type"
        verbose_name_plural = "Activity Type"
        
    def __str__(self):
        return self.activity_type
        
class Activity(models.Model):
    
    activity_type = models.ForeignKey(ActivityType, on_delete = models.CASCADE)
    point_on_map = gismodels.MultiPointField(srid = 4326, null = False, blank = False)
    start_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    activity_name = models.CharField(max_length = 64, blank = False, null = False)
    activity_fee = models.DecimalField(max_digits = 10, decimal_places = 2)
    activity_description = models.TextField()
    registration_deadline = models.DateField()
    location = models.CharField(max_length = 56, blank = False, null = False)
    image = models.ImageField(_("Images"), upload_to = upload_to, blank=True, null=True)
    members = models.ManyToManyField(Member)
    
    class Meta:
        verbose_name = "Activities"
        verbose_name_plural = "Activities"
    
    def __str__(self):
        return self.activity_name
    
class ActivityPhotos(models.Model):

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    photos = models.ImageField(upload_to = 'activities_gallery/', blank=True, null=True) 
    
    def __str__(self):
        return "Activity {} Photo uploaded by {} at {}".format(self.activity.activity_name, self.uploaded_by.first_name, self.uploaded_at)  
    