
from os import name
from django.urls import path
from . import views
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path('Materials/<str:course_name>/', views.AddMaterials),
path('uploadMaterial', views.AllMaterials),
path('addComment/<int:id>/', views.addComment,name='addComment'),
path('Materials/', views.Course, name = 'Course'),
path('Materials/course/del/<int:id>/', views.del_course),
path('uploadMaterial/<str:course_name>/', views.courseMaterial,name='courseMaterial'),
path('uploadMaterial/<str:course_name>/uploadMaterial/addComment/<int:id>/', views.courseMaterialComment),
path('Materials/<str:course_name>/deleteMaterial/<int:id>/',views.deleteMaterial),

url(r'^download/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
path('searchMaterials', views.searchMaterials,name='searchMaterials'),
path('searchMaterials/<int:id>/', views.searchMaterialComment),


]
if settings.DEBUG:

        urlpatterns+= static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
        urlpatterns= urlpatterns+ static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)