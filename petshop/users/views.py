from rest_framework.generics import ListAPIView

from petshop.utils.permissions import IsAdminUser
from .selectors import get_all_users
from .serializers import UserSerializer


class UsersListAPI(ListAPIView):
    queryset = get_all_users()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'username', 'phone_number', 'first_name', 'last_name']
