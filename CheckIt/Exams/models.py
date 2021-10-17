from HomePage.models import Courses
from django.contrib.auth.models import User
from django.db import models

from django.db.models.deletion import CASCADE
from HomePage.models import ExamFolder,Exams



# Create your models here.
class ExamScripts (models.Model):
    student_id = models.CharField(max_length = 100)
    pdf = models.FileField(upload_to = 'Scripts/')
    pdf_from_drive = models.CharField(max_length = 1000)
    title = models.CharField(max_length = 100)
    is_Checked = models.BooleanField(default = False)
    Marks = models.FloatField(default = 0)

    course_id = models.ForeignKey(Courses, on_delete = CASCADE)
    exam_id = models.ForeignKey(Exams, on_delete = CASCADE)
    owner_id = models.ForeignKey(User, on_delete = CASCADE)

    def __str__(self):
        return self.name

class UncheckedFile(models.Model):
    student_id = models.CharField(max_length=100)
    pdf= models.FileField(upload_to="files")
    is_checked = models.BooleanField(default=False)
    course_id = models.ForeignKey(Courses,on_delete=CASCADE)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)
    exam_id = models.ForeignKey(ExamFolder,on_delete=CASCADE)
    Marks = models.FloatField(default = 0)


    def __str__(self):
        return self.student_id


class ScriptDetails (models.Model):
    ques_no = models.CharField(max_length = 100)
    Marks = models.FloatField(default = 0)

    Script_id = models.ForeignKey(ExamScripts, on_delete = CASCADE)
    exam_id = models.ForeignKey(Exams, on_delete = CASCADE)

    def __str__(self):
        return self.name