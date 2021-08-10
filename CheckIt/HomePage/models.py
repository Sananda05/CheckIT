from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Courses (models.Model):
    name = models.CharField(max_length = 255)
    CourseCode = models.CharField(max_length = 255)

    owner_id = models.ForeignKey(User, on_delete = CASCADE)

    def __str__(self):
        return self.name

class ExamFolder(models.Model):
    exam_name = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    course_id = models.ForeignKey(Courses, on_delete = CASCADE)

    owner_id = models.ForeignKey(User, on_delete = CASCADE)  
       
