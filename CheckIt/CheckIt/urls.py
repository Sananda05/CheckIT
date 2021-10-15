from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('HomePage.urls')),
    path('', include('GoogleClassroom.urls')),
    path('', include('FrontEnd.urls')),
    path('', include('Materials.urls')),
    path('', include('ExamScripts.urls')),
]