from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'users'

profile = [
    path('', views.UserProfileRetrieveAPI.as_view(), name='user-profile'),
    path('update/', views.UserProfileUpdateAPI.as_view(), name='user-profile-update'),
    path('delete/', views.DeleteUserAccountAPI.as_view(), name='user-profile-delete'),
]

password = [
    path('change/', views.ChangePasswordAPI.as_view(), name='change-password'),
    path('set/', views.SetPasswordAPI.as_view(), name='set-password'),
    path('reset/', views.ResetPasswordAPI.as_view(), name='reset-password'),
]

urlpatterns = [
    path('', views.UsersListAPI.as_view(), name='users-list'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegisterAPI.as_view(), name='user-register'),
    path('verify/', views.UserVerificationAPI.as_view(), name='user-verify'),
    path('resend-verification-email/', views.ResendVerificationEmailAPI.as_view(), name='resend-verification-email'),
    path('resend-verification-sms/', views.ResendVerificationSMSAPI.as_view(), name='resend-verification-sms'),
    path('password/', include(password)),
    path('profile/', include(profile)),
]
