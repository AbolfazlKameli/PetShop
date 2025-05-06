from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from petshop.utils.doc_serializers import TokenResponseSerializer, ResponseSerializer
from petshop.utils.permissions import IsAdminUser, NotAuthenticatedUser, IsOwnerUser
from .selectors import (
    get_all_users,
    get_user_by_phone_number,
    get_user_by_email,
    get_user_by_id,
    get_all_addresses,
    get_user_addresses
)
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserVerificationSerializer,
    ResendVerificationEmailSerializer,
    ChangePasswordSerializer,
    SetPasswordSerializer,
    ResetPasswordSerializer,
    ResendVerificationSMSSerializer,
    MyTokenObtainPairSerializer,
    AddressSerializer
)
from .services import register, generate_otp_code, activate_user, change_user_password, update_user
from .tasks import send_email_task, send_sms_task


@extend_schema(responses={200: TokenResponseSerializer})
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom API for obtaining JWT tokens, with a limit of five requests per hour for each IP.
    """
    serializer_class = MyTokenObtainPairSerializer


class UsersListAPI(ListAPIView):
    """
    API for listing all users, accessible only to admin users.
    """
    queryset = get_all_users()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'username', 'phone_number', 'first_name', 'last_name']


class UserRegisterAPI(GenericAPIView):
    """
    API for user registration, accessible only to non-authenticated users,
    """
    serializer_class = UserRegisterSerializer
    permission_classes = (NotAuthenticatedUser,)

    @extend_schema(responses={201: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            vd = serializer.validated_data
            user = register(email=vd['email'], username=vd['username'], password=vd['password'])
            otp_code = generate_otp_code(email=user.email)
            content = f'Your verification code: \n{otp_code}'
            send_email_task.delay(
                email=user.email,
                content=content,
                subject='PetShop'
            )
            return Response(
                data={'data': {'message': 'We have sent a verification code to your email'}},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserVerificationAPI(GenericAPIView):
    """
    API for verifying user registration, accessible only to non-authenticated users,
    """
    serializer_class = UserVerificationSerializer
    permission_classes = (NotAuthenticatedUser,)

    @extend_schema(responses={200: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            email = serializer.validated_data.get('email')
            user = None
            if phone_number:
                user = get_user_by_phone_number(phone_number)
            elif email:
                user = get_user_by_email(email)
            if user is None:
                return Response(
                    data={'data': {'errors': 'User account with this credentials not found.'}},
                    status=status.HTTP_404_NOT_FOUND
                )

            if user.is_active:
                return Response(
                    data={'data': {'message': 'This account already is active'}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            activate_user(user=user)
            return Response(
                data={'data': {'message': 'Account activated successfully.'}},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class ResendVerificationEmailAPI(GenericAPIView):
    """
    API for resending a verification email, accessible only to non-authenticated users,
    """
    serializer_class = ResendVerificationEmailSerializer
    permission_classes = (NotAuthenticatedUser,)

    @extend_schema(responses={202: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = get_user_by_email(serializer.validated_data.get('email'))
            if user is None:
                return Response(
                    data={'data': {'message': 'User with this email not found.'}},
                    status=status.HTTP_404_NOT_FOUND
                )
            if user.is_active:
                return Response(
                    data={'data': {'message': 'This account already is active'}},
                    status=status.HTTP_400_BAD_REQUEST
                )

            otp_code = generate_otp_code(email=user.email)
            content = f'Your verification code: \n{otp_code}'
            send_email_task.delay(
                email=user.email,
                content=content,
                subject='PetShop'
            )
            return Response(
                data={'data': {'message': 'We have sent a verification code to your email'}},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class ResendVerificationSMSAPI(GenericAPIView):
    """
    API for resending a verification SMS, accessible only to non-authenticated users,
    """
    serializer_class = ResendVerificationSMSSerializer
    permission_classes = (NotAuthenticatedUser,)

    @extend_schema(responses={202: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            user = get_user_by_phone_number(phone_number=phone_number)
            if user is None:
                return Response(
                    data={'data': {'message': 'User with this phone numer not found'}},
                    status=status.HTTP_404_NOT_FOUND
                )
            if user.is_active:
                return Response(
                    data={'data': {'message': 'This account already is active'}},
                    status=status.HTTP_400_BAD_REQUEST
                )

            otp_code = generate_otp_code(phone_number=user.phone_number)
            content = f'Your verification code: \n{otp_code}'
            send_sms_task.delay(phone_number=phone_number, content=content)
            return Response(
                data={'data': {'message': 'We have sent you a verification code to your phone number.'}},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class ChangePasswordAPI(GenericAPIView):
    """
    API for changing a user's password, accessible only to the user.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsOwnerUser,)

    @extend_schema(responses={200: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            change_user_password(user=request.user, password=serializer.validated_data.get('confirm_password'))
            return Response(
                data={'data': {'message': 'Your password changed successfully.'}},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class SetPasswordAPI(GenericAPIView):
    """
    API for setting a user's password during the reset password process, accessible to all users.
    """
    serializer_class = SetPasswordSerializer
    permission_classes = (AllowAny,)

    @extend_schema(responses={200: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = get_user_by_email(serializer.validated_data.get('email'))
            if user is None:
                return Response(
                    data={'data': {'message': 'User with this email not found.'}},
                    status=status.HTTP_404_NOT_FOUND
                )
            change_user_password(user, serializer.validated_data.get('confirm_password'))
            return Response(
                data={'data': {'message': 'Password Set successfully.'}},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class ResetPasswordAPI(GenericAPIView):
    """
    API for initiating the password reset process by sending a reset link to the user's email, accessible to all users.
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    @extend_schema(responses={202: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = get_user_by_email(serializer.validated_data.get('email'))
            if user is None:
                return Response(
                    data={'data': {'message': 'User with this email not found.'}},
                    status=status.HTTP_404_NOT_FOUND
                )
            otp_code = generate_otp_code(email=user.email)
            content = f'Reset password code: \n{otp_code}'
            send_email_task.delay(
                email=user.email,
                content=content,
                subject='PetShop'
            )
            return Response(
                data={'data': {'message': 'We have sent a verification code to your email'}},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProfileRetrieveAPI(GenericAPIView):
    """
    API for retrieving the authenticated user's profile information.
    accessible only to the user themselves.
    """
    serializer_class = UserSerializer
    permission_classes = (IsOwnerUser,)

    def get(self, request, *args, **kwargs):
        user = get_user_by_id(user_id=request.user.id)
        if user is None:
            return Response(
                data={'data': {'message': 'User not found.'}},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(instance=user)
        return Response(
            data={'data': serializer.data},
            status=status.HTTP_200_OK
        )


class UserProfileUpdateAPI(GenericAPIView):
    """
    API for updating the authenticated user's profile.
    Includes support for updating email with re-verification if changed.
    Accessible to the user themselves.
    """
    serializer_class = UserSerializer
    permission_classes = (IsOwnerUser,)

    def get_object(self):
        user = get_user_by_id(self.request.user.id)
        if user is None:
            return Response(
                data={'data': {'message': 'User not found.'}},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_permissions(self.request)
        self.check_object_permissions(self.request, user)
        return user

    @extend_schema(responses={200: ResponseSerializer})
    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(instance=user, data=request.data)
        if serializer.is_valid():
            message, state = update_user(user, serializer.validated_data)

            if state == 1:
                otp_code = generate_otp_code(email=user.email)
                content = f'Your verification code: \n{otp_code}'
                send_email_task.delay(
                    email=user.email,
                    content=content,
                    subject='PetShop'
                )

            elif state == 2:
                otp_code = generate_otp_code(phone_number=user.phone_number)
                content = f'Your verification code: \n{otp_code}'
                send_sms_task.delay(phone_number=user.phone_number, content=content)

            return Response(
                data={'data': {'message': message}},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class DeleteUserAccountAPI(GenericAPIView):
    """
    API for deleting the authenticated user's account. Accessible to the user themselves.
    """
    permission_classes = (IsOwnerUser,)
    serializer_class = UserSerializer

    def get_object(self):
        user = get_user_by_id(self.request.user.id)
        if user is None:
            return Response(
                data={'data': {'message': 'User not found.'}},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_permissions(self.request)
        self.check_object_permissions(self.request, user)
        return user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAddressesListAPI(ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsOwnerUser,)
    search_fields = ('address', 'postal_code')

    def get_queryset(self):
        return get_user_addresses(owner=self.request.user)


class AddressCreateAPI(GenericAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                data={'data': {'message': 'address created successfully.'}},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class AddressUpdateAPI(GenericAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsOwnerUser,)
    lookup_url_kwarg = 'address_id'
    queryset = get_all_addresses()

    def put(self, request, *args, **kwargs):
        address = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=address)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'address updated successfully.'}},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class AddressDeleteAPI(GenericAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsOwnerUser,)
    lookup_url_kwarg = 'address_id'
    queryset = get_all_addresses()

    def delete(self, request, *args, **kwargs):
        address = self.get_object()
        address.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
