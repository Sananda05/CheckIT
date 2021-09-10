from django.urls import path
from django.utils.translation import templatize
from . import views
from .views import ChangePasswordView

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name = "src/Views/Authentication/Reset-Password/Password-Reset-Form.html"), 
        name ='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name = "src/Views/Authentication/Reset-Password/Password-Reset-done.html"), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = "src/Views/Authentication/Reset-Password/Password-Reset-confirm.html"),
        name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', views.Login_view),
    path('register/', views.Register_view),
    path('ChangePassword/', ChangePasswordView.as_view()),
    path('EditProfile/', views.EditProfile),
    path('<str:username>/', views.UserProfile),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)