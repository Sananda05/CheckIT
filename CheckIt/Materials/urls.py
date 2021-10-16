from . import views

from django.urls import path
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('Materials', views.Course, name = 'Course'),
    path('Materials/<str:course_name>/<str:course_id>', views.AddMaterials),
    path('Materials/<str:course_name>/<str:course_id>/deleteMaterial/<int:id>/',views.deleteMaterial),
    
    path('uploadMaterial', views.AllMaterials),
    path('uploadMaterial/<str:course_name>/', views.courseMaterial, name='courseMaterial'),
    path('uploadMaterial/<str:course_name>/uploadMaterial/addComment/<int:id>/', views.courseMaterialComment),

    path('addComment/<int:id>/', views.addComment, name='addComment'),
    url(r'^download/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    
    path('searchMaterials', views.searchMaterials,name='searchMaterials'),
    path('searchMaterials/<int:id>/', views.searchMaterialComment),
]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
    urlpatterns= urlpatterns+ static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)