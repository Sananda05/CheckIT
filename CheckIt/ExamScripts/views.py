from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import Courses, Exams, ExamScripts, ScriptDetails

def ExamView(request, coursename, examname):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = Exams.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        print(exam.exam_name)

        if request.method == "POST":
            #student_id = request.POST['student_id']
            pdf_name = request.FILES.getlist('exam_file')
            
            print(pdf_name)
            for file in pdf_name:
                ExamScripts.objects.create(pdf = file, owner_id_id = users.id, course_id_id = courses.id, exam_id_id = exam.id)
                
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
            for i in checkedExamScripts:
                checked_pdf_name = str(i.pdf).replace("Scripts/", "")
                checked_file_names.append(checked_pdf_name)
            
            print(checked_file_names)
            zipped_lists_2 = zip(checkedExamScripts, checked_file_names)

            return render(request, 'src/Views/Users/Exams/Exam.html', {'user' : users, 'courses' : courses, 'exam' : exam, 'examScripts' : examScripts, 'checkedExamScripts' : checkedExamScripts, "zipped_lists" : zipped_lists, "zipped_lists_2" : zipped_lists_2})
    else:
        return redirect("/login")

def ScriptView(request, coursename, examname, student_id):
    if request.user.is_authenticated :
        pdf_name = 'Scripts/'+ student_id
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = Exams.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        examScript = ExamScripts.objects.get( pdf = pdf_name, exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id )
        script_details = ScriptDetails.objects.filter(Script_id_id = examScript.id)

        if request.method == "POST":
            Marks = request.POST['Marks']
            studentId = request.POST['studentId']
            marks_details = request.POST.getlist('field_name[]')
            ques_no = request.POST.getlist('ques_no[]')

            zipped_list = zip(marks_details, ques_no)
            print(zipped_list)

            ExamScripts.objects.filter( id = examScript.id ).update( student_id = studentId, is_Checked = True, Marks = Marks )
            for mark, ques in zipped_list:
                ScriptDetails.objects.create(ques_no = ques, Marks = mark, Script_id_id = examScript.id, exam_id_id = exam.id)

            return redirect("/home/"+ coursename + "/" + examname)
        else:
            print(examScript.id)
            return render(request, 'src/Views/Users/Exams/ExamScript.html', {'user' : users, 'courses' : courses, 'exam' : exam, 'examScripts' : examScript, 'script_details' : script_details})
    else:
        return redirect("/login")

#def Uncheck(request, coursename, examname, student_id):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = Exams.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        examScript = ExamScripts.objects.get( student_id = student_id, exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id )

        ExamScripts.objects.filter( id = examScript.id ).update( is_Checked = False )

        return redirect("/home/"+ coursename + "/" + examname)
    
    else:
        return redirect("/login")

def Recheck(request, coursename, examname, student_id):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = Exams.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        examScript = ExamScripts.objects.get( student_id = student_id, exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id )
        script_details = ScriptDetails.objects.filter(Script_id_id = examScript.id)

        if request.method == 'POST':
            Marks = request.POST['Marks']
            marks_details = request.POST.getlist('field_name[]')
            ques_no = request.POST.getlist('ques_no[]')

            ExamScripts.objects.filter( id = examScript.id ).update( is_Checked = True, Marks = Marks )

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