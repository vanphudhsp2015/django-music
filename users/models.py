from django.db import models
from django.conf import settings

# Create your models here.
class AvatarUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='avatar', on_delete=models.CASCADE)
    avatar = models.FileField(upload_to = 'avatar/%Y/%m/%d/%H/%M/%S/',default='/default/default.png')

class Image(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='images',default='/photo.png')
