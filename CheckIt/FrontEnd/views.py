from django.shortcuts import render, redirect

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth.models import User
from HomePage.models import Courses, Exams
from ExamScripts.models import ExamScripts

from .forms import CreateUserForms

def index(request):
    return render(request, 'src/Views/home.html')

def Login_view(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/home')
        else:
            messages.info(request, 'User Not Found. Username or Password might be incorrect.')
            return redirect('/login')

    else:
        if request.user.is_authenticated :
            return redirect('/home')
        else:
            return render(request, 'src/Views/Authentication/LogIn.html')

def Register_view(request):
    RegisterForm = CreateUserForms()

    if request.method == 'POST':
        RegisterForm = CreateUserForms(request.POST)

        if RegisterForm.is_valid():
            RegisterForm.save()

            user = RegisterForm.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('/login')
        else: 
            messages.success(request, 'Something went Wrong. Username exists or Password is not too long. Please Try Again.')
            return redirect('/register')

    else:
        if request.user.is_authenticated :
            return redirect('/home')
        else:
            context = {'RegisterForm' : RegisterForm}
            return render(request, 'src/Views/Authentication/Register.html', context)

def UserProfile(request, username):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.filter( owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id )
        examScripts = ExamScripts.objects.filter( owner_id_id = users.id )

        if request.method == 'POST':
            password = request.POST['password']

            user = authenticate(username = username, password = password)
            if user is not None:
                print("Password is correct")

                request.session['passwordChecked'] = True
                passwordChecked = request.session.get('passwordChecked')
                print("After POST:")
                print(passwordChecked)
                return redirect('/EditProfile')
            else:
                messages.info(request, 'Password is incorrect.')
                return redirect('/' +  username)
        else:
            passwordChecked = False
            return render(request, 'src/Views/Users/User.html', {'username' : request.user, 'email' : users.email, 'courses' : courses, 'exams' : exams, 'examScripts' : examScripts})
    else:
        return redirect("/login")

def EditProfile(request):
    if request.user.is_authenticated:
        users = User.objects.get( username = request.user )
        courses = Courses.objects.filter( owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id )
        examScripts = ExamScripts.objects.filter( owner_id_id = users.id )

        if request.method == 'POST':
            name = request.POST['username']
            email = request.POST['email']
            print(name)
            print(email)

            User.objects.filter( id = users.id ).update( username = name, email = email )
        else:
            passwordChecked = request.session.get('passwordChecked')
            print ("Before: ")
            print (passwordChecked)
            if passwordChecked == True:
                request.session['passwordChecked'] = False
                print (passwordChecked)
                return render(request, 'src/Views/Users/Edit.html', {'username' : request.user, 'email' : users.email, 'courses' : courses, 'exams' : exams, 'examScripts' : examScripts})
            else:
                return redirect('/' + users.username)
    else:
        return redirect("/login")