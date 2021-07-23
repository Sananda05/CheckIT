from django.db import models
from django.contrib.auth.models import User

class UserProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    picture = models.ImageField((""), upload_to = 'ProfilePictures/', height_field=None, width_field=None, max_length=None)
    #models.Ima(upload_to = 'ProfilePictures/')