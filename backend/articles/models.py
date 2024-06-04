from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

def upload_to(instance, filename):
    return 'articles/cover_image/{filename}'.format(filename = filename)

def file_path(instance, filename):
    return 'articles/file/{filename}'.format(filename = filename)

class Article(models.Model):
    article_image = models.ImageField(_("Images"), upload_to = upload_to, blank=True, null=True)
    article_name = models.CharField(max_length = 128, blank=True, null=True)
    article_file = models.FileField(upload_to = file_path, blank=True, null=True)
    article_description = models.TextField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateField(auto_now_add = True)
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Article"
        