from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from petshop.utils.permissions import IsAdminUser, NotAuthenticatedUser, IsOwnerUser
from .selectors import get_all_users, get_user_by_phone_number, get_user_by_email
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserVerificationSerializer,
    ResendVerificationEmailSerializer,
    ChangePasswordSerializer,
    SetPasswordSerializer,
    ResetPasswordSerializer
)
from .services import register, generate_otp_code, activate_user, change_user_password
from .tasks import send_email


class UsersListAPI(ListAPIView):
    queryset = get_all_users()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'username', 'phone_number', 'first_name', 'last_name']


class UserRegisterAPI(GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (NotAuthenticatedUser,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            vd = serializer.validated_data
            user = register(email=vd['email'], username=vd['username'], password=vd['password'])
            otp_code = generate_otp_code(email=user.email)
            content = f'Your verification code: \n{otp_code}'
            send_email.delay(
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
    serializer_class = UserVerificationSerializer
    permission_classes = (NotAuthenticatedUser,)

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
    serializer_class = ResendVerificationEmailSerializer
    permission_classes = (NotAuthenticatedUser,)

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
            send_email.delay(
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


class ChangePasswordAPI(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsOwnerUser,)

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
    serializer_class = SetPasswordSerializer
    permission_classes = (NotAuthenticatedUser,)

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
    serializer_class = ResetPasswordSerializer
    permission_classes = (NotAuthenticatedUser,)

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
            send_email.delay(
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
