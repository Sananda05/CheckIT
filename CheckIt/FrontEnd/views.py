from django.contrib.messages.api import success
from django.forms import forms
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages

from django.contrib.auth.models import auth
from django.contrib.auth.models import User
from HomePage.models import Courses, Exams
from ExamScripts.models import ExamScripts
from .models import UserDetails, UserPictures
from allauth.socialaccount.models import SocialAccount

from .forms import CreateUserForms
from .models import UserDetails

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
        #else:
        #   users = User.objects.get( username = username )
        #    if users.last_login == '':
        #        redirect('/Set-Your-Profile')
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
            university = request.POST['university']

            user = RegisterForm.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            
            users = User.objects.get( username = user )
            print(users.username)
            print(users.id)
            UserDetails.objects.create( university = university, user_id = users.id )
            UserPictures.objects.create( user_id = users.id )

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
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        userDetails = UserDetails.objects.get( user_id = users.id )
        
        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        
        courses = Courses.objects.filter( owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id )
        examScripts = ExamScripts.objects.filter( owner_id_id = users.id )

        if request.method == 'POST':
            purpose = request.POST['purpose']

            if purpose == "Password-Check":
                password = request.POST['password']
                user = authenticate(username = username, password = password)
                if user is not None:
                    print("Password is correct")

                    request.session['passwordChecked'] = True
                    request.session['passwordChange'] = True

                    passwordChecked = request.session.get('passwordChecked')
                    print("After POST:")
                    print(passwordChecked)
                    return redirect('/EditProfile')
                else:
                    messages.info(request, 'Password is incorrect.')
                    return redirect('/' +  username)
            
            elif purpose == "Post-picture":
                profile_picture = request.FILES.get('profile_picture')

                UserPictures.objects.filter(user_id = users.id).delete()

                UserPictures.objects.create( picture = profile_picture, user_id = users.id)
                UserDetails.objects.filter( id = userDetails.id ).update( picture = profile_picture )
                     
                print(profile_picture)
                return redirect('/' +  username)
        else:
            request.session['passwordChange'] = False
            print(request.session['passwordChange'])

            if googleAcc == False:
                userPictures = UserPictures.objects.get( user_id = users.id )
                return render(request, 'src/Views/Users/User.html', {'no_picture' : no_picture, 'users': users,
                    'picture' : picture, 'username' : request.user, 'email' : users.email, 'courses' : courses, 
                    'exams' : exams, 'examScripts' : examScripts, 'userDetails' : userDetails, 'userPictures' : userPictures})
            else:
                return render(request, 'src/Views/Users/User.html', {'no_picture' : no_picture, 'users': users,
                    'picture' : picture, 'username' : request.user, 'email' : users.email, 'courses' : courses, 
                    'exams' : exams, 'examScripts' : examScripts, 'userDetails' : userDetails})
    else:
        return redirect("/login")

def EditProfile(request):
    if request.user.is_authenticated:
        users = User.objects.get( username = request.user )
        userDetails = UserDetails.objects.get( user_id = users.id )
        courses = Courses.objects.filter( owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id )
        examScripts = ExamScripts.objects.filter( owner_id_id = users.id )
        socialaccount_obj = SocialAccount.objects.filter(provider='google', user_id = users.id)
        userPictures = UserPictures.objects.get(user_id = users.id)
        
        picture = "not available"
        no_picture = "not available"

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
        
        print(picture)

        if request.method == 'POST':
            purpose = request.POST['purpose']

            if purpose == "Edit-Info":
                name = request.POST['username']
                university = request.POST['university']
                firstName = request.POST['firstName']
                lastName = request.POST['lastName']
            
                print(name)
                print(firstName)
                print(lastName)

                User.objects.filter( id = users.id ).update( username = name, first_name = firstName, last_name = lastName )
                UserDetails.objects.filter( user_id = users.id ).update( university = university )
            
                return redirect('/' + users.username)
            elif purpose == "Post-picture":
                profile_picture = request.FILES.get('profile_picture')

                UserPictures.objects.filter(user_id = users.id).delete()

                UserPictures.objects.create( picture = profile_picture, user_id = users.id)
                UserDetails.objects.filter( id = userDetails.id ).update( picture = profile_picture )
                     
                print(profile_picture)
                return redirect('/EditProfile') 
            elif purpose == "Delete-picture":
                UserPictures.objects.filter(user_id = users.id).update( picture = '' )
                UserDetails.objects.filter( id = userDetails.id ).update( picture = '' )
                     
                return redirect('/EditProfile') 
        else:
            passwordChecked = request.session.get('passwordChecked')
            print ("Before: ")
            print (passwordChecked)
            
            #if passwordChecked == True or googleAcc == True:
             #   request.session['passwordChecked'] = False
              #  print (passwordChecked)
            
            return render(request, 'src/Views/Users/Edit.html', 
                {'no_picture' : no_picture, 'picture' : picture, 'users': users, 'courses' : courses, 
                'exams' : exams, 'examScripts' : examScripts, 'userDetails': userDetails, 'userPictures': userPictures})
            #else:
             #   return redirect('/' + users.username)
    else:
        return redirect("/login")

#def ChangePassword(request):
    if request.user.is_authenticated:
        users = User.objects.get( username = request.user )
        courses = Courses.objects.filter( owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id )
        examScripts = ExamScripts.objects.filter( owner_id_id = users.id )

        if request.method == 'POST':
            o_password = request.POST['o_password']
            password = request.POST['password']
            c_password = request.POST['c_password']

            print(o_password)
            print(password)
            print(c_password)
            username = (users.username)
            user = authenticate(username = username, password = password)
            if user is not None:
                if (password == c_password):
                    User.objects.filter( id = users.id ).update(password = password)
                    print("Password updated successfully")
                    return redirect('/' + users.username)
                else:
                    messages.success(request, 'Something went Wrong. Password was not confirmed. Please Try Again.')
                    print("Something went Wrong. Password was not confirmed. Please Try Again.")
                    return redirect('/' + users.username)
            else:
                messages.success(request, 'Something went Wrong. Please Try Again.')
                print("Something went Wrong. Please Try Again.")
                return redirect('/' + users.username)
        else:
            passwordChange = request.session.get('passwordChange')
            print ("Before: ")
            print (passwordChange)
            if passwordChange == True:
                request.session['passwordChange'] = False
                print (passwordChange)
                return render(request, 'src/Views/Users/ChangePW.html', {'username' : request.user, 'email' : users.email, 'courses' : courses, 'exams' : exams, 'examScripts' : examScripts})
            else:
                return redirect('/' + users.username)
    else:
        return redirect("/login")

class ChangePasswordView (PasswordChangeView):
    template_name = 'src/Views/Users/ChangePW.html'
    success_url = reverse_lazy('Home')

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial = self.initial, user = request.user)
        users = User.objects.get( username = request.user )
        userDetails = UserDetails.objects.get( user_id = users.id )
        socialaccount_obj = SocialAccount.objects.filter(provider='google', user_id = users.id)
        userPictures = UserPictures.objects.get(user_id = users.id)
        
        picture = "not available"
        no_picture = "not available"

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
        
        return render(request, self.template_name, {'form': form, 'no_picture' : no_picture, 'picture' : picture, 'users': users, 
            'userDetails': userDetails, 'userPictures': userPictures})