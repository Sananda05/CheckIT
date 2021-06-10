from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CreateUserForms

# Create your views here.

def index(request):
    return render(request, 'src/Templates/home.html')

def Login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.info(request, 'User Not Found. Username or Password might be incorrect.')

    return render(request, 'src/Templates/Authentication/LogIn.html')

def Register_view(request):
    RegisterForm = CreateUserForms()

    if request.method == 'POST':
        RegisterForm = CreateUserForms(request.POST)
        if RegisterForm.is_valid():
            RegisterForm.save()

            user = RegisterForm.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('/login')

    context = {'RegisterForm' : RegisterForm}
    return render(request, 'src/Templates/Authentication/Register.html', context)
