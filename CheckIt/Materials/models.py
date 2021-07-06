from django.db import models
from django.db.models.deletion import CASCADE
from HomePage.models import User

# Create your models here.

class materials(models.Model):
    uni_name = models.CharField(max_length=300)
    course_name = models.CharField(max_length=50)
    description = models.TextField()
    username =models.TextField()

    owner_id = models.ForeignKey(User, on_delete=CASCADE)
