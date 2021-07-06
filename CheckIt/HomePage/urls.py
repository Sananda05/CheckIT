from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomePage),
    path('logout/', views.Logout),
    path('addCourse/', views.AddCourse),
    path('<str:coursename>/addExam/', views.AddExam),
    path('<str:username>/', views.UserProfile),
    path('home/<str:coursename>/', views.CourseView),
]