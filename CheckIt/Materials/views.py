from Materials.models import materials
from django.shortcuts import redirect, render
from HomePage.models import User

# Create your views here.

def AddMaterials (request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )

        if request.method == "POST":

            uni_name = request.POST['university'],
            course_name = request.POST['coursename'],
            description = request.POST['description']

            materials.objects.create(uni_name=uni_name, course_name=course_name, username = users.username,description=description, owner_id_id = users.id)
            return redirect("/Materials")

        elif request.method == "GET":
            material = materials.objects.filter(owner_id_id = users.id)
            return render(request, "src/Views/Materials/addMaterials.html", {'material':material, 'name' : users.username})   
    else:
        return render("/login")


def AllMaterials (request):
    material = materials.objects.all()
    return render(request, "src/Views/Materials/AllMaterials.html", {'material':material})