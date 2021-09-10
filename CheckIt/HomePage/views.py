from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from FrontEnd.models import UserPictures, UserDetails

from .models import Courses, Exams
from ExamScripts.models import ExamScripts

def HomePage(request):
    print (request.user)

    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        userPictures = UserPictures.objects.get( user = users.id )
        userDetails = UserDetails.objects.get( user_id = users.id )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        courses = Courses.objects.filter( owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id )
        
        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        
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
            return render(request, 'src/Views/Home/HomeContent.html', 
            {'user' : users, 'userPictures' : userPictures, 'courses' : courses, "zipped_lists" : zipped_lists,
            'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc, 'userDetails': userDetails})
    else:
       return redirect("/login")

def CourseView(request, coursename):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        userPictures = UserPictures.objects.get( user = users.id )

        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id, course_id_id = courses.id )
        scripts = ExamScripts.objects.filter( owner_id_id = users.id, course_id_id = courses.id )
        
        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        
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
            exam_question = request.FILES.get('exam_question')

            print(exam_name)
            print(exam_question)
                
            #Exams.objects.create(exam_name = exam_name, course_id_id = course_id, owner_id_id = owner_id)
            Exams.objects.create(exam_name = exam_name, exam_question = exam_question, course_id_id = course_id, owner_id_id = owner_id)
                
            print(users.username + " added exam " + exam_name + " under course " + courses.name)

            return redirect('/home/'+ courses.name)
        else:
            zipped_lists = zip(exams, script_count)
            return render(request, 'src/Views/Home/Course.html', 
            {'user' : users, 'userPictures': userPictures,  'coursename' : courses.name, 'exams' : exams, "zipped_lists" : zipped_lists,
            'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc})
    else:
        return redirect("/login")

def Logout(request):
    print (request.user, "logging out")

    if request.method == "POST":
       return render(request, 'src/Views/Home/Homepage.html') 
    else:
       logout(request)
       return redirect("/login")

def SetProfile(request):
    print (request.user)

    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        userPictures = UserPictures.objects.get( user = users.id )
        userDetails = UserDetails.objects.get( user_id = users.id )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )        
        
        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True        
        
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
            return render(request, 'src/Views/Users/NewUser.html', 
            {'user' : users, 'userPictures' : userPictures, 'picture': picture, 'no_picture': no_picture,
             'googleAcc': googleAcc, 'userDetails': userDetails})
    else:
       return redirect("/login")