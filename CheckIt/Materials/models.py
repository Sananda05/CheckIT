from django.db import models
from django.db.models.deletion import CASCADE
from HomePage.models import User
from embed_video.fields import EmbedVideoField



# Create your models here.
class course_list(models.Model):
    
    course_name = models.CharField(max_length=50)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)


    def __str__(self):
        return self.student_id
    

class materials(models.Model):
    uni_name = models.CharField(max_length=300)
    
    description = models.TextField()
    username =models.TextField()
    pdf= models.FileField(upload_to="File")
    video=models.TextField()
    course_name=models.CharField(max_length=50)
    course_id=models.ForeignKey(course_list,on_delete=CASCADE)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)
