from django.contrib.auth.models import User
from django.http import response
from HomePage.models import Courses, ExamFolder
from .models import UncheckedFile,ScriptDetails
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.

def AddExamfile (request, exam_name, coursename ):
    if request.user.is_authenticated :
      users = User.objects.get( username = request.user )
      courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
      examFolders = ExamFolder.objects.get(exam_name = exam_name, owner_id_id = courses.id)
     

      if request.method == "POST":
                #student_id = request.POST['student_id']
                pdf = request.POST.getlist('exam_file')
              
                print(pdf)
                for file in pdf:
                  UncheckedFile.objects.create( pdf=file,owner_id_id = users.id, course_id_id=courses.id, exam_id_id= examFolders.id)
                return redirect("/Course/"+ coursename + "/" + exam_name)

      elif request.method == "GET":
                unchecked = UncheckedFile.objects.filter(owner_id_id = users.id, course_id= courses.id, exam_id_id= examFolders.id,is_checked=False)

                checkedExamScripts = UncheckedFile.objects.filter( exam_id_id = examFolders.id, owner_id_id = users.id, course_id_id = courses.id, is_checked = True )
                return render(request, 'src/Views/Exams/AddExamFile.html' , {'unchecked':unchecked, 'exam_name':exam_name, "checkedExamScripts":checkedExamScripts})  
    else:
        return redirect("/login")     

def ScriptView(request, coursename, examname, student_id):
    if request.user.is_authenticated :
        
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = ExamFolder.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        examScript = UncheckedFile.objects.get( pdf = student_id, exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id )
        script_details = ScriptDetails.objects.filter(Script_id_id = examScript.id)

        if request.method == "POST":
            Marks = request.POST['Marks']
            studentId = request.POST['studentId']
            marks_details = request.POST.getlist('field_name[]')
            ques_no = request.POST.getlist('ques_no[]')

            zipped_list = zip(marks_details, ques_no)
            print(zipped_list)

            UncheckedFile.objects.filter( id = examScript.id ).update( student_id = studentId, is_Checked = True, Marks = Marks )
            for mark, ques in zipped_list:
                ScriptDetails.objects.create(ques_no = ques, Marks = mark, Script_id_id = examScript.id, exam_id_id = exam.id)

            return redirect("/home/"+ coursename + "/" + examname)
        else:
            print(examScript.id)
            return render(request, 'src/Views/Exams/ExamScripts.html', {'user' : users, 'courses' : courses, 'exam' : exam, 'examScripts' : examScript, 'script_details' : script_details})
    else:
        return redirect("/login")             


def Recheck(request, coursename, examname, student_id):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = ExamFolder.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        examScript = UncheckedFile.objects.get( student_id = student_id, exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id )
        script_details = ScriptDetails.objects.filter(Script_id_id = examScript.id)

        if request.method == 'POST':
            Marks = request.POST['Marks']
            marks_details = request.POST.getlist('field_name[]')
            ques_no = request.POST.getlist('ques_no[]')

            UncheckedFile.objects.filter( id = examScript.id ).update( is_checked = True, Marks = Marks )

            zipped_list = zip(marks_details, ques_no)
            print(zipped_list)
            for mark, ques in zipped_list:
                if mark != "" and ques != "":                    
                    if ScriptDetails.objects.filter(Script_id_id = examScript.id, ques_no = ques).exists():
                        ScriptDetails.objects.filter( Script_id_id = examScript.id, ques_no = ques ).update( Marks = mark )
                    else:
                        ScriptDetails.objects.create(ques_no = ques, Marks = mark, Script_id_id = examScript.id, exam_id_id = exam.id)
                        
            return redirect("/home/"+ coursename + "/" + examname)

        else:
            return render(request, 'src/Views/Users/Exams/EditMarks.html', {'user' : users, 'courses' : courses, 'exam' : exam, 'examScripts' : examScript, 'script_details' : script_details})
    
    else:
        return redirect("/login")










