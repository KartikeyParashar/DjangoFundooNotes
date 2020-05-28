from django.urls import path

from . import views

urlpatterns = [
    path('user/register/', views.RegistrationAPIView.as_view(), name='register'),
    path('activate/<token>/', views.activate, name='activate'),
    path('user/login/', views.LoginAPIView.as_view(), name='login'),
    path('user/reset_password/', views.ResetPasswordAPIView.as_view(), name='reset_password'),
    path('verify/<token>/', views.verify, name='verify'),
    path('user/forgot_password/<ResetUser>/', views.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('user/logout/', views.Logout.as_view(), name='logout'),
    path('user/social_login/', views.SocialLogin.as_view(), name='social_login'),
    path('new/', views.access_token, name='social'),
    path('user/image_upload/', views.UploadImage.as_view(), name='image_upload'),
]

