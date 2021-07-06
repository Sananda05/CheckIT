from django.db import models
from django.db.models.deletion import CASCADE

from django.contrib.auth.models import User
from HomePage.models import Courses, Exams

class ExamScripts (models.Model):
    student_id = models.CharField(max_length = 100, unique = True)
    pdf = models.FileField(upload_to = 'Scripts/')
    is_Checked = models.BooleanField(default = False)
    Marks = models.IntegerField(default = 0)

    course_id = models.ForeignKey(Courses, on_delete = CASCADE)
    exam_id = models.ForeignKey(Exams, on_delete = CASCADE)
    owner_id = models.ForeignKey(User, on_delete = CASCADE)

    def __str__(self):
        return self.name