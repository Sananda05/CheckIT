from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def HomePage(request, *args, **kwargs):
    #return HttpResponse("Hello!")
    return render(request, 'home.html', {})
