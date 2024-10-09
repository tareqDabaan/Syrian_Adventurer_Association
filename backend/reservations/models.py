# Django imports 
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local modules imports
from users.models import User 
from activities.models import Activity

class Request(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    )
    participant_id = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE) ##NOT CORRECT
    activity_id = models.ForeignKey(Activity, blank=True, null=True, on_delete = models.CASCADE)
    request_created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length = 200, blank=True, null=True, choices = STATUS, default = 'Pending')
    # payment 
    
class AcceptedReservations(models.Model):
    user = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE) 
    activity_id = models.ForeignKey(Activity, blank=True, null=True, on_delete = models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True, blank=True, null=True) 
    
class RejectedReservations(models.Model):
    user = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE) 
    activity_id = models.ForeignKey(Activity, blank=True, null=True, on_delete = models.CASCADE)
    rejected_at = models.DateTimeField(auto_now_add=True, blank=True, null=True) 
    reason = models.TextField()