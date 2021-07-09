from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.contrib.auth.models import User
from .models import Courses, Exams
from ExamScripts.models import ExamScripts

def HomePage(request):
    print (request.user)

    if request.user.is_authenticated :
        users = User.objects.get( username = request.user ) 
        courses = Courses.objects.filter( owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id )
        
        exam_count = []
        for course in courses:
            count = 0
            for exam in exams:
                if exam.course_id_id == course.id:
                    count = count + 1
            exam_count.append(count)
        
        if request.method == "POST":
            owner_id = users.id
                
            name = request.POST.get('name')
            CourseCode = request.POST.get('CourseCode')

            print(name)
            print(CourseCode)
                
            Courses.objects.create(name = name, CourseCode = CourseCode, owner_id_id = owner_id)
                
            print(users.username + " added Course " + name)

            return redirect('/home')
            
        else:
            zipped_lists = zip(courses, exam_count)
            return render(request, 'src/Views/Home/HomeContent.html', {'user' : users, 'courses' : courses, "zipped_lists" : zipped_lists})
    else:
       return redirect("/login")

def AddCourse(request):
    print (request.user)

    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        
        if request.method == "POST":
            owner_id = users.id
                
            name = request.POST.get('name')
            CourseCode = request.POST.get('CourseCode')

            print(name)
            print(CourseCode)
                
            Courses.objects.create(name = name, CourseCode = CourseCode, owner_id_id = owner_id)
                
            print(users.username + " added Course " + name)

            return redirect('/home')
        else:
            courses = Courses.objects.filter( owner_id_id = users.id ) 
            return render(request, 'src/Views/Home/AddCourse.html', {'user' : users, 'courses' : courses})
    else:
       return redirect("/login")

def AddExam(request, coursename):
    print (request.user)

    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        
        if request.method == "POST":
            owner_id = users.id
            course_id = courses.id    
            exam_name = request.POST.get('exam_name')

            print(exam_name)
                
            Exams.objects.create(exam_name = exam_name, course_id_id = course_id, owner_id_id = owner_id)
                
            print(users.username + " added exam " + exam_name + " under course " + courses.name)

            return redirect('/Course/'+ courses.name)
        else:
            return render(request, 'src/Views/Users/Exams/AddExam.html', {'username' : request.user, 'email' : users.email, 'coursename' : courses.name})
    else:
       return redirect("/login")

def CourseView(request, coursename):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id, course_id_id = courses.id )
        scripts = ExamScripts.objects.filter( owner_id_id = users.id, course_id_id = courses.id )
        
        script_count = []
        for exam in exams:
            count = 0
            for script in scripts:
                if script.exam_id_id == exam.id:
                    count = count + 1
            script_count.append(count)
        print(script_count)
        
        if request.method == "POST":
            owner_id = users.id
            course_id = courses.id    
            exam_name = request.POST.get('exam_name')

            print(exam_name)
                
            Exams.objects.create(exam_name = exam_name, course_id_id = course_id, owner_id_id = owner_id)
                
            print(users.username + " added exam " + exam_name + " under course " + courses.name)

            return redirect('/home/'+ courses.name)
        else:
            zipped_lists = zip(exams, script_count)
            return render(request, 'src/Views/Users/Course.html', {'user' : users, 'coursename' : courses.name, 'exams' : exams, "zipped_lists" : zipped_lists})
    else:
        return redirect("/login")

def Logout(request):
    print (request.user, "logging out")

    if request.method == "POST":
       return render(request, 'src/Views/Home/Homepage.html') 
    else:
       logout(request)
       return redirect("/login")