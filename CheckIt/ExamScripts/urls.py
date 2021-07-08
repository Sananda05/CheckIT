from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/<str:coursename>/<str:examname>/', views.ExamView),
    path('home/<str:coursename>/<str:examname>/Script<str:student_id>/', views.ScriptView),
    #path('home/<str:coursename>/<str:examname>/Script<str:student_id>/Review/uncheck/', views.Uncheck),
    path('home/<str:coursename>/<str:examname>/Script<str:student_id>/Review/', views.Recheck),
]
   
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)