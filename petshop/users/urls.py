from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .apis import auth

app_name = 'users'

profile = [
    path('', views.UserProfileRetrieveAPI.as_view(), name='user-profile'),
    path('update/', views.UserProfileUpdateAPI.as_view(), name='user-profile-update'),
    path('delete/', views.DeleteUserAccountAPI.as_view(), name='user-profile-delete'),
    path('addresses/', views.UserAddressesListAPI.as_view(), name='user-addresses-list'),
]

password = [
    path('change/', views.ChangePasswordAPI.as_view(), name='change-password'),
    path('set/', views.SetPasswordAPI.as_view(), name='set-password'),
    path('reset/', views.ResetPasswordAPI.as_view(), name='reset-password'),
]

addresses = [
    path('create/', views.AddressCreateAPI.as_view(), name='address-create'),
    path('<int:address_id>/update/', views.AddressUpdateAPI.as_view(), name='address-update'),
    path('<int:address_id>/delete/', views.AddressDeleteAPI.as_view(), name='address-delete'),
]

urlpatterns = [
    path('', views.UsersListAPI.as_view(), name='users-list'),
    path('login/', auth.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', auth.UserRegisterAPI.as_view(), name='user-register'),
    path('verify/', auth.UserVerificationAPI.as_view(), name='user-verify'),
    path('resend-verification-email/', auth.ResendVerificationEmailAPI.as_view(), name='resend-verification-email'),
    path('resend-verification-sms/', auth.ResendVerificationSMSAPI.as_view(), name='resend-verification-sms'),
    path('password/', include(password)),
    path('profile/', include(profile)),
    path('addresses/', include(addresses)),
]
