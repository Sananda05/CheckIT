from django.urls import path
from . import views
from .views import ChangePasswordView

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('login/', views.Login_view),
    path('register/', views.Register_view),
    path('ChangePassword/', ChangePasswordView.as_view()),
    path('EditProfile/', views.EditProfile),
    path('<str:username>/', views.UserProfile),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)