from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home-classroom/', views.GC_HomePage, name = 'GC-Home'),
    path('authorize/', views.GC_authorize),
    path('oauth2callback/', views.GC_oauth2callback, name = 'oauth2callback'),
    path('home-classroom/<str:course_id>/', views.GC_CourseView),
    path('home-classroom/<str:course_id>/<str:courseWork_id>/', views.GC_submissions),
    path('home-classroom/<str:course_id>/<str:courseWork_id>/<str:script_id>/', views.GC_file),
    path('home-classroom/<str:course_id>/<str:courseWork_id>/graded/<str:script_id>/<str:id>', views.GC_gradedFile),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)