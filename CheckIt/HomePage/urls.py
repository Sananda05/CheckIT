from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/', views.HomePage, name = 'Home'),
    path('home-classroom/', views.GC_HomePage, name = 'GC-Home'),
    path('authorize/', views.GC_authorize),
    path('oauth2callback/', views.GC_oauth2callback, name = 'oauth2callback'),

    path('Set-Your-Profile/', views.SetProfile, name = 'Set-Your-Profile'),
    path('logout/', views.Logout),
    path('home/<str:coursename>/', views.CourseView),
    path('home-classroom/<str:course_id>/', views.GC_CourseView),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)