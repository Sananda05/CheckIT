from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomePage),
    path('logout/', views.Logout),
    path('addCourse/', views.AddCourse),
    path('<str:username>/', views.UserProfile),
    path('Course/<str:coursename>/', views.CourseView),
]