
from django.urls import path
from . import views

urlpatterns = [

path('Materials', views.AddMaterials),
path('uploadMaterial', views.AllMaterials),

]