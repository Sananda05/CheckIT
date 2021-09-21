from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
# Create your models here.

class uploaded_pdfFile(models.Model):
    student_id = models.CharField(max_length=100)
    pdf= models.FileField(upload_to="compare_files")
    is_compared = models.BooleanField(default=False)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)


    def __str__(self):
        return self.student_id

class history(models.Model):
    pdf1= models.FileField(upload_to="compare_history")
    pdf2= models.FileField(upload_to="compare_history")
    rate= models.CharField(max_length=200)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)


    def __str__(self):
        return self.student_id


