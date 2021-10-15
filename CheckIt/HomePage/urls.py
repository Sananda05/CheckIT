from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/', views.HomePage, name = 'Home'),
    path('Set-Your-Profile/', views.SetProfile, name = 'Set-Your-Profile'),
    path('logout/', views.Logout),
    path('home/<str:coursename>/', views.CourseView),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)