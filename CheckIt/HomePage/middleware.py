from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class checkUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __isLoggedin__(self, request):
        if request.method == 'POST':
        
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('/home')
            else:
                messages.redirect('/login')
        
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response