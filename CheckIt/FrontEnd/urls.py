from django.urls import path
from . import views
from .views import ChangePasswordView

urlpatterns = [
    path('', views.index),
    path('login/', views.Login_view),
    path('register/', views.Register_view),
    path('ChangePassword/', ChangePasswordView.as_view()),
    path('EditProfile/', views.EditProfile),
    path('<str:username>/', views.UserProfile),
]