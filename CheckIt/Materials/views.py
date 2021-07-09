from .models import materials
from django.shortcuts import redirect, render
from HomePage.models import User
from django.http import HttpResponse
import os
from django.conf import settings
from django.http.response import Http404


# Create your views here.

def AddMaterials (request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )

        if request.method == "POST":

            uni_name = request.POST["university"],
            course_name = request.POST['coursename'],
            description = request.POST['description'],
            pdf= request.FILES['exam_file']
            video=request.POST['vid_file'] #getting the value from html file

            #print(video)
            #print(f"Debug URL :>>>{video}<<<")

            materials.objects.create(uni_name=uni_name, course_name=course_name, username = users.username,description=description, pdf=pdf, owner_id_id = users.id, video=video) # storing in database
            return redirect("/Materials")

        elif request.method == "GET":
            
            material = materials.objects.filter(owner_id_id = users.id)
            return render(request, "src/Views/Materials/addMaterials.html", {'material':material, 'name' : users.username})   
    else:
        return render("/login")


def AllMaterials (request):
    material = materials.objects.all()
    return render(request, "src/Views/Materials/AllMaterials.html", {'material':material})

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path,'rb') as pdf:
            response=HttpResponse(pdf.read(), content_type="application/pdf")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response

    raise Http404            