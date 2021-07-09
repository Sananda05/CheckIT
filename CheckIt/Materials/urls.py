from . import views

from django.urls import path
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('Materials', views.AddMaterials),
    path('uploadMaterial', views.AllMaterials),
    url(r'^download/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    path('searchMaterials', views.searchMaterials,name='searchMaterials'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
    urlpatterns= urlpatterns+ static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)