from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):
    picture = models.ImageField((""), upload_to = 'ProfilePictures/', 
                                      height_field = None, width_field = None, max_length = None)
    university = models.CharField(max_length = 255)

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    #models.Ima(upload_to = 'ProfilePictures/')

class UserPictures(models.Model):
    picture = models.ImageField((""), upload_to = 'ProfilePictures/', 
                                      height_field = None, width_field = None, max_length = None)

    user = models.OneToOneField(User, on_delete = models.CASCADE)