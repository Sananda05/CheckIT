from django.contrib.auth.models import User
from django.http import response
from HomePage.models import Courses, ExamFolder
from .models import UncheckedFile
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.

def AddExamfile (request, exam_name, coursename ):
    if request.user.is_authenticated :
      users = User.objects.get( username = request.user )
      courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
      examFolders = ExamFolder.objects.get(exam_name = exam_name, owner_id_id = courses.id)
     

      if request.method == "POST":
                student_id = request.POST['student_id']
                pdf = request.POST['exam_file']
              
            
                print(student_id)
                print(pdf)

                UncheckedFile.objects.create(student_id=student_id, pdf=pdf,owner_id_id = users.id, course_id_id=courses.id, exam_id_id= examFolders.id)
                return redirect("/Course/"+ coursename + "/" + exam_name)

      elif request.method == "GET":
                unchecked = UncheckedFile.objects.filter(owner_id_id = users.id, course_id= courses.id, exam_id_id= examFolders.id)
                return render(request, 'src/Views/Exams/AddExamFile.html' , {'unchecked':unchecked, 'exam_name':exam_name})  
    else:
        return redirect("/login")          


#def checkExamfile(request, pdf):
 #  with open('/checkExamFile/to/'+pdf, 'rb') as pdf:
  #      response = HttpResponse(pdf.read(),content_type='application/pdf')
   #     response['Content-Disposition'] = 'filename=some_file.pdf'
    #    return response










