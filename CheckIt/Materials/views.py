import os

from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render

from django.conf import settings
from django.contrib import messages

from .models import User, materials

def AddMaterials (request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )

        if request.method == "POST":

            uni_name = request.POST["university"],
            course_name = request.POST['coursename'],
            description = request.POST['description'],
            pdf = request.FILES['exam_file']
            video = request.POST['vid_file'] #getting the value from html file

            #print(video)
            #print(f"Debug URL :>>>{video}<<<")

            materials.objects.create(uni_name=uni_name, course_name=course_name, username = users.username,description=description, pdf=pdf, owner_id_id = users.id, video=video) # storing in database
            return redirect("/Materials")

        elif request.method == "GET":
            
            material = materials.objects.filter(owner_id_id = users.id)
            return render(request, "src/Views/Materials/addMaterials.html", {'material': material, 'name' : users.username})   
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

def searchMaterials(request):
    query=request.GET['query']
    if len(query)>78:
        AllMaterials=materials.objects.none()
    else:
        AllMaterialsCourse=materials.objects.filter(course_name__icontains=query)
        AllMaterialsUni_name=materials.objects.filter(uni_name__icontains=query)
        AllMaterials=AllMaterialsCourse.union(AllMaterialsUni_name)

    if AllMaterials.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
        
    params={'AllMaterials':AllMaterials,'query':query}
    return render(request, "src/Views/Materials/searchMaterials.html",params)
