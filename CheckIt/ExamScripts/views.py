from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import Courses, Exams, ExamScripts

def ExamView(request, coursename, examname):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = Exams.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        print(exam.exam_name)

        if request.method == "POST":
                student_id = request.POST['student_id']
                pdf = request.FILES['exam_file']
            
                print(student_id)
                print(pdf)

                ExamScripts.objects.create(student_id = student_id, pdf = pdf, owner_id_id = users.id, course_id_id = courses.id, exam_id_id = exam.id)
                return redirect("/home/"+ coursename + "/" + examname)
        
        else:
            examScripts = ExamScripts.objects.filter( exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id, is_Checked = False )
            file_names = []
            for i in examScripts:
                pdf_name = str(i.pdf).replace("Scripts/", "")
                file_names.append(pdf_name)
            
            print(file_names)
            zipped_lists = zip(examScripts, file_names)

            checkedExamScripts = ExamScripts.objects.filter( exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id, is_Checked = True )
            checked_file_names = []
            for i in examScripts:
                checked_pdf_name = str(i.pdf).replace("Scripts/", "")
                checked_file_names.append(checked_pdf_name)
            
            print(checked_file_names)
            zipped_lists_2 = zip(checkedExamScripts, checked_file_names)

            return render(request, 'src/Views/Users/Exams/Exam.html', {'user' : users, 'courses' : courses, 'exam' : exam, 'examScripts' : examScripts, 'checkedExamScripts' : checkedExamScripts, "zipped_lists" : zipped_lists, "zipped_lists_2" : zipped_lists_2})
    else:
        return redirect("/login")

def ScriptView(request, coursename, examname, student_id):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = Exams.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        examScript = ExamScripts.objects.get( student_id = student_id, exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id )

        return render(request, 'src/Views/Users/Exams/ExamScript.html', {'user' : users, 'courses' : courses, 'exam' : exam, 'examScripts' : examScript})
