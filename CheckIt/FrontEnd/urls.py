from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.index,name='google_login'),
   # path('accounts/',include('allauth.urls')),
    path('login/', views.Login_view),
    path('register/', views.Register_view),
    
]