from HomePage.models import Courses
from django.contrib.auth.models import User
from django.db import models

from django.db.models.deletion import CASCADE
from HomePage.models import ExamFolder



# Create your models here.

class UncheckedFile(models.Model):
    student_id = models.CharField(max_length=100)
    pdf= models.FileField(upload_to="unchekedScripts")
    is_checked = models.BooleanField(default=False)
    course_id = models.ForeignKey(Courses,on_delete=CASCADE)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)
    exam_id = models.ForeignKey(ExamFolder,on_delete=CASCADE)

    def __str__(self):
        return self.student_id


