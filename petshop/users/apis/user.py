from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.exceptions import CustomNotFound
from petshop.utils.permissions import IsAdminUser, IsOwnerUser
from ..selectors import (
    get_all_users,
    get_user_by_email,
    get_user_by_id
)
from ..serializers import (
    UserSerializer,
    ChangePasswordSerializer,
    SetPasswordSerializer,
    ResetPasswordSerializer
)
from ..services import generate_otp_code, change_user_password, update_user
from ..tasks import send_email_task, send_sms_task


class UsersListAPI(ListAPIView):
    """
    API for listing all users, accessible only to admin users.
    """
    queryset = get_all_users()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'username', 'phone_number', 'first_name', 'last_name']


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
            raise CustomNotFound('User not found.')

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
            raise CustomNotFound('User not found.')

        self.check_object_permissions(self.request, user)
        return user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
