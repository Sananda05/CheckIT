from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.contrib.auth.models import User
from .models import Courses, ExamFolder

def HomePage(request):
    print (request.user)

    if request.user.is_authenticated :
        users = User.objects.get( username = request.user ) 
        courses = Courses.objects.filter( owner_id_id = users.id )
        print(users)
        print(courses)
        
        return render(request, 'src/Views/Home/HomeContent.html', {'username' : request.user, 'email' : users.email, 'courses': courses})
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
            return render(request, 'src/Views/Home/AddCourse.html', {'username' : request.user, 'email' : users.email})
    else:
       return redirect("/login")

def UserProfile(request, username):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.filter( owner_id_id = users.id )

        return render(request, 'src/Views/Users/User.html', {'username' : request.user, 'email' : users.email, 'courses' : courses})
    else:
        return redirect("/login")      

def CourseView(request, coursename):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )

        print(courses.id)

        if request.method == "POST":

            
           #owner_id = users.id
           # course_id = courses.id

            exam_name = request.POST['exam_name']
            semester = request.POST['semester']

            print(exam_name)
            print(semester)

            ExamFolder.objects.create(exam_name= exam_name, semester=semester,owner_id_id = courses.id)
            print(courses.id)
           
            return redirect("/Course/"+courses.name)

        elif request.method == "GET":
             exams = ExamFolder.objects.filter(owner_id_id= courses.id)
             return render(request, 'src/Views/Users/Course.html', {'exams' : exams,'coursename' : coursename})
    else :
        return redirect("/login")    

def delete_exam (request,id):
    if request.method == "POST":
        exam = ExamFolder.objects.get(id=id)
        exam.delete()            

def Logout(request):
        print (request.user, "logging out")

        if request.method == "POST":
             return render(request, 'src/Views/Home/Homepage.html') 
        else:
            logout(request)
            return redirect("/login")