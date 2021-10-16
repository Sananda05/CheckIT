from django.db import models
from django.db.models.deletion import CASCADE

from django.contrib.auth.models import User

from django.db.models.deletion import CASCADE

class course_list(models.Model):
    course_name = models.CharField(max_length=100)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)

class materials(models.Model):
    uni_name = models.CharField(max_length = 300)
    course_name = models.CharField(max_length = 50)
    description = models.TextField()
    username =models.TextField()
    pdf= models.FileField(upload_to = "File/")
    video=models.TextField()

    owner_id = models.ForeignKey(User, on_delete = CASCADE)
    course_id=models.ForeignKey(course_list,on_delete=CASCADE)

class Comment(models.Model):
    material_id = models.ForeignKey(materials,on_delete=CASCADE)
    username=models.CharField(max_length=50)
    user_picture = models.ImageField((""), upload_to = 'Comment-ProfilePictures/', 
                height_field = None, width_field = None, max_length = None)
    text = models.TextField()
    googleAcc = models.CharField(max_length=50)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
   

    class Meta:
        ordering = ['created_at']