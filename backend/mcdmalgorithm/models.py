# Django imports 
from django.db import models
from django.utils.translation import gettext_lazy as _

    
class Dataset(models.Model):
    budget = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    preferred_month = models.CharField(max_length=20, blank=True, null=True)
    preferred_places = models.CharField(max_length=256, null=True, blank=True) 
    preferred_types = models.CharField(max_length=256, null=True, blank=True)  
    preferred_difficulity = models.CharField(max_length=256, null=True, blank=True)
    more_than_day = models.BooleanField(default=False, blank=True, null=True)
    
    class Meta:
        verbose_name = "User Preference"
        verbose_name_plural = "User Preferences"