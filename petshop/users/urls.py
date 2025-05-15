from django.urls import path, include

from .apis import auth, user, address

app_name = 'users'

profile = [
    path('', user.UserProfileRetrieveAPI.as_view(), name='user-profile'),
    path('update/', user.UserProfileUpdateAPI.as_view(), name='user-profile-update'),
    path('delete/', user.DeleteUserAccountAPI.as_view(), name='user-profile-delete'),
    path('addresses/', address.UserAddressesListAPI.as_view(), name='user-addresses-list'),
]

password = [
    path('change/', user.ChangePasswordAPI.as_view(), name='change-password'),
    path('set/', user.SetPasswordAPI.as_view(), name='set-password'),
    path('reset/', user.ResetPasswordAPI.as_view(), name='reset-password'),
]

addresses = [
    path('create/', address.AddressCreateAPI.as_view(), name='address-create'),
    path('<int:address_id>/update/', address.AddressUpdateAPI.as_view(), name='address-update'),
    path('<int:address_id>/delete/', address.AddressDeleteAPI.as_view(), name='address-delete'),
]

urlpatterns = [
    path('', user.UsersListAPI.as_view(), name='users-list'),
    path('login/', auth.CustomTokenObtainPairAPI.as_view(), name='token_obtain_pair'),
    path('refresh/', auth.CustomTokenRefreshAPI.as_view(), name='token_refresh'),
    path('register/', auth.UserRegisterAPI.as_view(), name='user-register'),
    path('verify/', auth.UserVerificationAPI.as_view(), name='user-verify'),
    path('<int:user_id>/ban/', auth.BanUserAPI.as_view(), name='user-ban'),
    path('resend-verification-email/', auth.ResendVerificationEmailAPI.as_view(), name='resend-verification-email'),
    path('resend-verification-sms/', auth.ResendVerificationSMSAPI.as_view(), name='resend-verification-sms'),
    path('password/', include(password)),
    path('profile/', include(profile)),
    path('addresses/', include(addresses)),
]
