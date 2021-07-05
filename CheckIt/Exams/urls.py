
from django.urls import path
from . import views

urlpatterns = [

path('Course/<str:coursename>/<str:exam_name>/', views.AddExamfile),
#path('<str:pdf>', views.viewFile)
#path('checkExamFile/to/<str:pdf>', views.checkExamfile)
]