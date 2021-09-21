from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class pdfFiles(models.Model):
    student_id = models.CharField(max_length=100)
    pdf= models.FileField(upload_to="pdffiles")
    is_converted = models.BooleanField(default=False)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)


    def __str__(self):
        return self.student_id

class ConvertedPdfFile(models.Model):
    textfile = models.FileField(blank=True)

    student_id = models.CharField(max_length=100)
   
    owner_id = models.ForeignKey(User, on_delete=CASCADE)


    def __str__(self):
        return self.student_id       

class HandWrittenFiles(models.Model):
    student_id = models.CharField(max_length=100)
    pdf= models.FileField(upload_to="handwrittenfiles")
    is_converted = models.BooleanField(default=False)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)


    def __str__(self):
        return self.student_id

class ConvertedHandwrittenFile(models.Model):
    textfile = models.FileField(blank=True)

    student_id = models.CharField(max_length=100)
   
    owner_id = models.ForeignKey(User, on_delete=CASCADE)


    def __str__(self):
        return self.student_id

