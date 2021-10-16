import os

from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.db.models.fields import PositiveBigIntegerField

from django.conf import settings
from django.contrib import messages

from .models import User, materials, Comment, course_list
from allauth.socialaccount.models import SocialAccount
from FrontEnd.models import UserPictures

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def Course(request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        userPictures = UserPictures.objects.get( user = users.id )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )

        courses = course_list.objects.filter(owner_id_id = users.id )
        material = materials.objects.filter( owner_id_id = users.id )

        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        
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
            {'user' : users,'courses' : courses, "zipped_lists" : zipped_lists, 'userPictures': userPictures,
            'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc})
    else:
       return redirect("/login")

def addComment(request,id):
    material=materials.objects.get(id=id)
    comments=Comment.objects.filter(material_id_id=material.id,  parent=None)
    Material=materials.objects.filter(id=id)
    
    if request.method=='POST':
        comment=request.POST['comment']
        material_id=material.id
        googleAcc = False

        if request.user.is_authenticated :
            username=request.user
            users = User.objects.get(username = request.user)
            userPictures = UserPictures.objects.get( user = users.id )
            socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
            
            picture = "not available"
            googleAcc = False

            if len(socialaccount_obj):
                picture = socialaccount_obj[0].extra_data['picture']
                googleAcc = True
            
            if googleAcc == False:
                picture = userPictures.picture
        else:
            username='Viewer'
            picture='' 
        parentid=request.POST['parentid']
        if parentid:
            parent=Comment.objects.get(id=parentid)
            newcom=Comment(text=comment,username=username, material_id_id = material_id,parent=parent)
            newcom.save()
        else:
            newcom=Comment(text=comment,username=username,material_id_id = material_id, user_picture=picture, googleAcc=googleAcc)
            newcom.save()

        return redirect('/addComment/'+str(material.id))
    elif request.method == "GET":
        userPictures = ""
        picture = ""
        no_picture = ""
        googleAcc = False

        if request.user.is_authenticated :
            is_loggedIn = 'Yes'
            username=request.user
            users = User.objects.get(username = request.user)
            userPictures = UserPictures.objects.get( user = users.id )
            socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
            
            picture = "not available"
            no_picture = "not available"
            googleAcc = False

            if len(socialaccount_obj):
                picture = socialaccount_obj[0].extra_data['picture']
                googleAcc = True
        else:
            is_loggedIn = 'No'

        return render(request, "src/Views/Materials/Comment.html", {'Material':Material,'comments':comments, 'is_loggedIn': is_loggedIn,
        'userPictures': userPictures,
            'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc})

def AddMaterials (request, course_name, course_id):
    if request.user.is_authenticated:
        users = User.objects.get( username = request.user )
        userPictures = UserPictures.objects.get( user = users.id )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        
        courses = course_list.objects.get(id = course_id)
        comments = Comment.objects.filter(parent=None)

        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True

        if request.method == "POST":
            uni_name = request.POST['university']
            course_name = courses.course_name
            description = request.POST['description']
            pdf = request.FILES['exam_file']
            video = request.POST['vid_file'] #getting the value from html file

            #print(video)
            #print(f"Debug URL :>>>{video}<<<")

            materials.objects.create(uni_name = uni_name, course_id_id = course_id, course_name = course_name, username = users.username, description = description, pdf = pdf, owner_id_id = users.id, video = video) # storing in database
            return redirect("/Materials/" + course_name + "/" + course_id)

        elif request.method == "GET":
            material = materials.objects.filter(owner_id_id = users.id, course_id_id = course_id)
            
            page = request.GET.get('page')
            paginator = Paginator(material,2)

            try:
                material = paginator.page(page)
            except PageNotAnInteger:
                material = paginator.page(1)
            except EmptyPage:
                material = paginator.page(paginator.num_pages)
            
            return render(request, "src/Views/Materials/addMaterials.html", 
            {'material': material, 'name' : users.username, 'userPictures': userPictures,
            'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc, 'courses': courses,
            'page':page, 'comments':comments})   
    else:
        return render("/login")

def AllMaterials (request):
    material = materials.objects.all()
    courseList = course_list.objects.all()
    comments=Comment.objects.filter(parent=None)

    return render(request, "src/Views/Materials/AllMaterials.html", { 'material': material, 'list':courseList, 'comments': comments })

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline;filename =' + os.path.basename(file_path)
            return response

    raise Http404 

def searchMaterials(request):
    query = request.GET['query']
    
    if len(query) > 78:
        AllMaterials = materials.objects.none()
    else:
        AllMaterialsCourse=materials.objects.filter(course_name__icontains=query)
        AllMaterialsUni_name=materials.objects.filter(uni_name__icontains=query)
        AllMaterials=AllMaterialsCourse.union(AllMaterialsUni_name)

    if AllMaterials.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
        
    params = {'AllMaterials': AllMaterials, 'query': query}
    
    return render(request, "src/Views/Materials/searchMaterials.html", params)

def deleteMaterial(request, course_name, course_id, id):
    if request.user.is_authenticated :
        material = materials.objects.get(id = id)
        material.delete()

        return redirect('/Materials/'+ course_name + '/' + course_id)

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