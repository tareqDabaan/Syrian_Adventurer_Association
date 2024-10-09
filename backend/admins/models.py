from django.db import models

# Django imports 
from django.db import models
from django.utils.translation import gettext_lazy as _

class Messages(models.Model):
    
    name = models.CharField(max_length = 256, blank=True, null=True)    
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateField(auto_now_add=True, blank=True, null=True)
    is_spam = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  
    
    class Meta:
        verbose_name = "Messages"
        verbose_name_plural = "Messages"
        
    def __str__(self):
        return f"{self.email}, {self.name}"