# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

def upload_to(instance, filename):
    return 'our_gallery/{filename}'.format(filename = filename)

class Gallery(models.Model):
    image = models.ImageField(_("Images"), upload_to=upload_to, blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateField(auto_now_add = True)
    description = models.TextField()
    