from django.urls import path
from . import views
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path('compare/multiplefiles', views.Multiplefiles),
path('compare/twofiles',views.Twofiles),
path('comparison/history',views.historyView),
path('compare/files/result', views.ComparePdf),
path('compare/multiple/result', views.CompareMultiple),
path('compare/files/del/<int:id>', views.deletePdf),
path('compare/files/reset/files/', views.reset),
path('comparison/history/del/<int:id>', views.deleteHistory),

]

if settings.DEBUG:

        urlpatterns+= static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
        urlpatterns= urlpatterns+ static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)