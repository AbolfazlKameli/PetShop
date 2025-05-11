from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from petshop.utils.permissions import IsOwnerOrAdminUser
from .serializers import OrderSerializer
from .selectors import get_all_orders


class OrderRetrieveAPI(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsOwnerOrAdminUser,)
    lookup_url_kwarg = 'order_id'
    queryset = get_all_orders()

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.serializer_class(instance=order)
        return Response(
            data={'data': serializer.data},
            status=status.HTTP_200_OK
        )
