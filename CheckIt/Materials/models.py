from django.db import models
from django.contrib.auth.models import User

from django.db.models.deletion import CASCADE

class materials(models.Model):
    uni_name = models.CharField(max_length = 300)
    course_name = models.CharField(max_length = 50)
    description = models.TextField()
    username =models.TextField()
    pdf= models.FileField(upload_to = "File/")
    video=models.TextField()

    owner_id = models.ForeignKey(User, on_delete = CASCADE)