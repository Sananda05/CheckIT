from django.db import models
from django.db.models.deletion import CASCADE
from HomePage.models import User
from embed_video.fields import EmbedVideoField

# Create your models here.

class materials(models.Model):
    uni_name = models.CharField(max_length=300)
    course_name = models.CharField(max_length=50)
    description = models.TextField()
    username =models.TextField()
    pdf= models.FileField(upload_to="materials_file")
    video=models.TextField()

    owner_id = models.ForeignKey(User, on_delete=CASCADE)


class course_list(models.Model):
    
    course_name = models.CharField(max_length=50)
    

    
