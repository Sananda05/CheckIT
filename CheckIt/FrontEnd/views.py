from django.shortcuts import render, redirect

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib import messages

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
