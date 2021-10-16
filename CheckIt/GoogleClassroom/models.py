from django.db import models
from django.db.models.deletion import CASCADE

from django.contrib.auth.models import User

# Create your models here.
class GC_ExamScripts (models.Model):
    scriptID = models.CharField(max_length = 200)
    courseWorkID = models.CharField(max_length = 200)
    courseID = models.CharField(max_length = 200)
    student_id = models.CharField(max_length = 100)

    is_Checked = models.BooleanField(default = False)
    Marks = models.FloatField(default = 0)

    owner_id = models.ForeignKey(User, on_delete = CASCADE)

    def __str__(self):
        return self.name

class GC_ScriptDetails (models.Model):
    ques_no = models.CharField(max_length = 100)
    Marks = models.FloatField(default = 0)
    script = models.CharField(max_length = 200)


    Script_id = models.ForeignKey(GC_ExamScripts, on_delete = CASCADE)

    def __str__(self):
        return self.name
