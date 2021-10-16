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

class uploaded_multipleFile1(models.Model):
    pdf= models.FileField(upload_to="compare_multiplefile")
    is_compared = models.BooleanField(default=False)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)

       

class uploaded_multipleFile(models.Model):
    pdf= models.FileField(upload_to="compare_multiple")
    is_compared = models.BooleanField(default=False)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)

    


class history(models.Model):
    pdf1= models.FileField(upload_to="compare_history")
    pdf2= models.FileField(upload_to="compare_history")
    rate= models.CharField(max_length=200)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)




class multiple_history(models.Model):
    pdf1= models.FileField(upload_to="files")
    pdf2= models.FileField(upload_to="files")
    rate= models.CharField(max_length=200)
    pdf2_id = models.ForeignKey(uploaded_multipleFile, on_delete=CASCADE)
    owner_id = models.ForeignKey(User, on_delete=CASCADE)


  



