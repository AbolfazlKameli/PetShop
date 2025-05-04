from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from petshop.utils.permissions import IsAdminUser, NotAuthenticatedUser
from .selectors import get_all_users
from .serializers import UserSerializer, UserRegisterSerializer
from .services import register, generate_otp_code
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
