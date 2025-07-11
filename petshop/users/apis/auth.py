from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from petshop.utils.doc_serializers import TokenResponseSerializer, ResponseSerializer
from petshop.utils.exceptions import CustomNotFound, CustomBadRequest
from petshop.utils.permissions import NotAuthenticatedUser, IsAdminUser
from ..selectors import get_user_by_phone_number, get_user_by_email, get_all_users
from ..serializers import (
    UserRegisterSerializer,
    UserVerificationSerializer,
    ResendVerificationEmailSerializer,
    ResendVerificationSMSSerializer,
    MyTokenObtainPairSerializer,
    UserSerializer
)
from ..services import register, generate_otp_code, activate_user, deactivate_user
from ..tasks import send_email_task, send_sms_task


@extend_schema(tags=['Auth'])
class CustomTokenRefreshAPI(TokenRefreshView):
    """
    Custom API for refreshing JWT tokens.
    """


@extend_schema(responses={200: TokenResponseSerializer}, tags=['Auth'])
class CustomTokenObtainPairAPI(TokenObtainPairView):
    """
    Custom API for obtaining JWT tokens, with a limit of five requests per hour for each IP.
    """
    serializer_class = MyTokenObtainPairSerializer


@extend_schema(tags=['Auth'])
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
            otp_code = generate_otp_code(email=user.email, action='verify')
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
        raise CustomBadRequest(serializer.errors)


@extend_schema(tags=['Auth'])
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
            if phone_number is not None:
                user = get_user_by_phone_number(phone_number)
            elif email is not None:
                user = get_user_by_email(email)
            else:
                user = None
            response = Response(
                data={'data': {'message': 'Account activated successfully.'}},
                status=status.HTTP_200_OK
            )
            if user is None:
                return response
            if user.is_active:
                raise CustomBadRequest('This account already is active.')

            activate_user(user=user)
            return response
        raise CustomBadRequest(serializer.errors)


@extend_schema(tags=['Auth'])
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
            response = Response(
                data={'data': {'message': 'We have sent a verification code to your email'}},
                status=status.HTTP_202_ACCEPTED
            )
            if user is None:
                return response
            if user.is_active:
                raise CustomBadRequest('This account already is active.')

            otp_code = generate_otp_code(email=user.email, action='verify')
            content = f'Your verification code: \n{otp_code}'
            send_email_task.delay(
                email=user.email,
                content=content,
                subject='PetShop'
            )
            return response
        raise CustomBadRequest(serializer.errors)


@extend_schema(tags=['Auth'])
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
            response = Response(
                data={'data': {'message': 'We have sent you a verification code to your phone number.'}},
                status=status.HTTP_202_ACCEPTED
            )
            if user is None:
                return response
            if user.is_active:
                raise CustomBadRequest('This account already is active.')

            otp_code = generate_otp_code(phone_number=user.phone_number, action='verify')
            content = f'Your verification code: \n{otp_code}'
            send_sms_task.delay(phone_number=phone_number, content=content)
            return response
        raise CustomBadRequest('This account already is active.')


@extend_schema(tags=['Auth'])
class BanUserAPI(GenericAPIView):
    """
    API for banning Users. Accessible only to the admins.
    """
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    queryset = get_all_users()
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        deactivate_user(user=user)
        return Response(
            data={'data': {'message': 'User banned successfully.'}},
            status=status.HTTP_200_OK
        )
