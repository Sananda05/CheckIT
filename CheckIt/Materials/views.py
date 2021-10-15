from django.shortcuts import redirect, render
from HomePage.models import User
from django.http import HttpResponse
import os
from django.conf import settings
from django.http.response import Http404
from django.contrib import messages

from .models import materials,course_list,course_folder
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger



# Create your views here.

def Course(request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courseslist = course_list.objects.all()
        courses = course_folder.objects.all()
        material = materials.objects.filter( owner_id_id = users.id )
        
        material_count = []
        for course in courses:
            count = 0
            for Material in material:
                if Material.course_id_id == course.id:
                    count = count + 1
            material_count.append(count)
        
        if request.method == "POST":
            owner_id = users.id
                
            course_name = request.POST.get('course_name')
            coursefolder = request.POST.get('coursename')
            print(coursefolder)
            print(course_name)
            
            if coursefolder!= "Select Course":
             course_folder.objects.create(course_name= coursefolder, owner_id_id = owner_id)   
            course_list.objects.create(course_name = course_name, owner_id_id = owner_id)
            print(users.username + " added Course " + course_name)
                
            return redirect('/Materials')
            
        else:
            zipped_lists = zip(courses, material_count)
            return render(request, 'src/Views/Materials/Courses.html', 
            {'user' : users,'courselist' : courseslist, "coursefolder":courses, "zipped_lists" : zipped_lists})
    else:
       return redirect("/login")



def AddMaterials(request, course_name):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )

        courses = course_list.objects.get( course_name = course_name )
        material = materials.objects.filter( owner_id_id = users.id, course_id_id = courses.id )
        
        if request.method == "POST":
            owner_id = users.id
            course_id = courses.id
            course_name=courses.course_name
            uni_name = request.POST["university"],
            description = request.POST['description'],
            pdf= request.FILES.get('exam_file')
            video=request.POST['vid_file'] 

            
            materials.objects.create(uni_name=uni_name, course_id_id = course_id, course_name=course_name,username = users.username,description=description, pdf=pdf, owner_id_id = users.id, video=video) # storing in database   
           
            return redirect('/Materials/'+ courses.course_name)


            
        elif request.method == "GET":

         material = materials.objects.filter(owner_id_id = users.id, course_id_id = courses.id)
         courses = course_list.objects.all()
            #pagination
         page=request.GET.get('page')
         paginator=Paginator(material,2)

         try:
            material=paginator.page(page)
         except PageNotAnInteger:
            material=paginator.page(1)
         except EmptyPage:
           material=paginator.page(paginator.num_pages)
        return render(request, "src/Views/Materials/addMaterials.html", {'material':material, 'name' : users.username,'courses':courses,'page':page})
    else:
        return redirect("/login")

def AllMaterials (request):
    material = materials.objects.all()
    courseList = course_list.objects.all()
    return render(request, "src/Views/Materials/AllMaterials.html", {'material':material,'list':courseList})
 #   comments=Comment.objects.filter(active=True)
  #  new_comment=None
   # if request.method=='POST':
       # comment_form=CommentForm(data=request.POST)
       # if comment_form.is_valid():
          # new_comment=comment_form.save(commit=False)
          # new_comment.material=material
          # new_comment.save()
          # return HttpResponseRedirect('/Materials'+material)
    #else:
       # comment_form=CommentForm()

#pagination
   # page=request.GET.get('page')
   # paginator=Paginator(material,2)

   # try:
       # material=paginator.page(page)
   # except PageNotAnInteger:
      #  material=paginator.page(1)
    #except EmptyPage:
       # material=paginator.page(paginator.num_pages)

   # return render(request, "src/Views/Materials/AllMaterials.html", {'material':material,'comments':comments,'new_comment':new_comment ,'comment_form':comment_form ,'page':page})

#def download(request, path):
    #file_path = os.path.join(settings.MEDIA_ROOT, path)
    #if os.path.exists(file_path):
        #with open(file_path,'rb') as pdf:
            #response=HttpResponse(pdf.read(), content_type="application/pdf")
            #response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
           # return response

    #raise Http404 

def searchMaterials(request):
    params={}
    query=request.GET['query']
    if len(query)>78:
        AllMaterials=materials.objects.none()
    else:
        AllMaterialsCourse=materials.objects.filter(course_name__icontains=query)
        AllMaterialsUni_name=materials.objects.filter(uni_name__icontains=query)
        AllMaterialsDescription=materials.objects.filter(description__icontains=query)
        AllMaterials=AllMaterialsCourse.union(AllMaterialsUni_name,AllMaterialsDescription)
        
    if AllMaterials.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
     
    #pagination
    page=request.GET.get('page')
    paginator=Paginator(AllMaterials,2)

    try:
        AllMaterials=paginator.page(page)
    except PageNotAnInteger:
        AllMaterials=paginator.page(1)
    except EmptyPage:
        AllMaterials=paginator.page(paginator.num_pages)
    return render(request, "src/Views/Materials/searchMaterials.html",{'AllMaterials':AllMaterials,'query':query,'page':page}) 




def deleteMaterial(request,course_name, id):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = course_list.objects.get( course_name=course_name, owner_id_id = users.id )
        material = materials.objects.get(id=id)
        material.delete()

        return redirect('/Materials/'+ courses.course_name)

    else:
        return redirect("/login")


def courseMaterial (request, course_name):
    courses = course_list.objects.get(course_name=course_name)
    material = materials.objects.filter(course_name = courses.course_name)

    #pagination
    page=request.GET.get('page')
    paginator=Paginator(material,2)

    try:
        material=paginator.page(page)
    except PageNotAnInteger:
        material=paginator.page(1)
    except EmptyPage:
        material=paginator.page(paginator.num_pages)
    
    return render(request, "src/Views/Materials/courseMaterials.html", {'material':material,'couses':courses,'page':page})