from django.urls import path
from . import views
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path('conversion/handwrittenfiles', views.Handwrittenfiles),
path('conversion/pdffiles',views.Pdffiles),
path('conversion/handwrittenfiles/<str:pdf>/',views.ConvertHandwrittenPdf),
path('conversion/pdffiles/<str:pdf>/',views.ConvertPdf),
path('conversion/download/<str:file_name>/', views.download_file),
path('conversion/handwrittenfiles/delconverted/<int:id>/',views.DeleteWrittenConvertedFile),
path('conversion/handwrittenfiles/del/<int:id>/',views.DeleteWrittenUnConvertedFile),
path('conversion/pdffiles/delconverted/<int:id>/',views.DeleteConvertedFile),
path('conversion/pdffiles/del/<int:id>/',views.DeleteUnConvertedFile),

]

if settings.DEBUG:

        urlpatterns+= static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
        urlpatterns= urlpatterns+ static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)