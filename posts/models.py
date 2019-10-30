from django.db import models
from django.utils import timezone

# Create your models here.
class Posts(models.Model):
  title = models.CharField(max_length=250,default='Default')
  images = models.FileField(upload_to = 'posts/%Y/%m/%d',default='/photo.png')
  author = models.CharField(max_length=250,default='author')
  categories = models.CharField(max_length=250,default='categories')
  tags = models.CharField(max_length=250,default='tags')
  visibility = models.CharField(max_length=250,default='public')
  commnets = models.IntegerField(default=0)
  views =  models.IntegerField(default=0)
  date_create = models.DateTimeField(default=timezone.now, blank=True)

  def __str__(self):
      return self.title + '-' + self.author


class Images(models.Model):
  images = models.FileField(upload_to = 'posts/%Y/%m/%d',default='/photo.png')
