from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.UsersListAPI.as_view(), name='users-list'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegisterAPI.as_view(), name='user-register'),
    path('verify/', views.UserVerificationAPI.as_view(), name='user-verify'),
    path('resend-verification-email/', views.ResendVerificationEmailAPI.as_view(), name='resend-verification-email'),
]
