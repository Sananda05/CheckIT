from django.urls import reverse
from django.db.models.fields import PositiveBigIntegerField
from .models import materials,Comment,course_list

from django.shortcuts import redirect, render
from HomePage.models import User
from django.http import HttpResponse
import os
import urllib.parse
from django.conf import settings
from django.http.response import Http404, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.

def Course(request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = course_list.objects.all()
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
            print(course_name)
            
                
            course_list.objects.create(course_name = course_name, owner_id_id = owner_id)
            print(users.username + " added Course " + course_name)
                
            return redirect('/Materials')
            
        else:
            zipped_lists = zip(courses, material_count)
            return render(request, 'src/Views/Materials/Courses.html', 
            {'user' : users,'courses' : courses, "zipped_lists" : zipped_lists})
    else:
       return redirect("/login")



def AddMaterials(request, course_name):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        comments=Comment.objects.filter(parent=None)

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
        return render(request, "src/Views/Materials/addMaterials.html", {'material':material, 'name' : users.username,'courses':courses,'page':page,'comments':comments})
    else:
        return redirect("/login")


def addComment(request,id):
    material=materials.objects.get(id=id)
    comments=Comment.objects.filter(material_id_id=material.id,  parent=None)
    Material=materials.objects.filter(id=id)
    if request.method=='POST':
        comment=request.POST['comment']
        material_id=material.id
        
        if request.user.is_authenticated :
            username=request.user
        else:
            username='Viewer'
        parentid=request.POST['parentid']
        if parentid:
            parent=Comment.objects.get(id=parentid)
            newcom=Comment(text=comment,username=username, material_id_id = material_id,parent=parent)
            newcom.save()
        else:
            newcom=Comment(text=comment,username=username,material_id_id = material_id)
            newcom.save()

        return redirect('/addComment/'+str(material.id))
    elif request.method == "GET":
        return render(request, "src/Views/Materials/Comment.html", {'Material':Material,'comments':comments})




def AllMaterials (request):
    
    Materials = materials.objects.all()
    courseList = course_list.objects.all()
    #m= []
    comments=Comment.objects.filter(parent=None)
    #for material in Materials:
    #    comments=Comment.objects.filter(material_id_id= material.id,parent=None)

    #    c=[]
    #    for comment in comments:
            
    #        c.append(comment.username)
    #        c.append(comment.text)
    #        c.append(comment.created_at)
    #    m.append(c)
    
    #print('comments')
    #print(m)
    
    #zipped_lists = zip(Materials, m)
    

    return render(request, "src/Views/Materials/AllMaterials.html", {'material':Materials,'list':courseList, 'comments': comments#,'zipped_lists':zipped_lists, 
    })
 



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
    comments=Comment.objects.filter(parent=None)
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
    return render(request, "src/Views/Materials/searchMaterials.html",{'AllMaterials':AllMaterials,'query':query,'page':page,'comments':comments}) 




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
    comments=Comment.objects.filter(parent=None)
    #pagination
    page=request.GET.get('page')
    paginator=Paginator(material,2)

    try:
        material=paginator.page(page)
    except PageNotAnInteger:
        material=paginator.page(1)
    except EmptyPage:
        material=paginator.page(paginator.num_pages)
    
    return render(request, "src/Views/Materials/courseMaterials.html", {'material':material,'courses':courses,'page':page,'comments':comments})

def courseMaterialComment(request,course_name,id):
    page = request.GET.get('page', '')
    courses = course_list.objects.get(course_name=course_name)
    material=materials.objects.get(id=id)
    if request.method=='POST':
        comment=request.POST['comment']
        material_id=material.id
        
        if request.user.is_authenticated :
            username=request.user
        else:
            username='Viewer'
        parentid=request.POST['parentid']
        if parentid:
            parent=Comment.objects.get(id=parentid)
            newcom=Comment(text=comment,username=username, material_id_id = material_id,parent=parent)
            newcom.save()
        else:
            newcom=Comment(text=comment,username=username,material_id_id = material_id)
            newcom.save()
        
        return redirect('/uploadMaterial/'+courses.course_name +'/?page='+str(page))


def searchMaterialComment(request,id):
    query=request.GET.get('query')
    material=materials.objects.get(id=id)
   
    if request.method=='POST':
        comment=request.POST['comment']
        material_id=material.id
        
        if request.user.is_authenticated :
            username=request.user
        else:
            username='Viewer'
        parentid=request.POST['parentid']
        if parentid:
            parent=Comment.objects.get(id=parentid)
            newcom=Comment(text=comment,username=username, material_id_id = material_id,parent=parent)
            newcom.save()
        else:
            newcom=Comment(text=comment,username=username,material_id_id = material_id)
            newcom.save()

    return redirect('/searchMaterials/?query='+str(query))



