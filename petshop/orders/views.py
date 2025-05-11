from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from petshop.utils.permissions import IsOwnerOrAdminUser
from .models import Order
from .selectors import get_all_orders
from .serializers import OrderSerializer, OrderListSerializer


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


class UserOrdersListAPI(ListAPIView):
    permission_classes = (IsOwnerOrAdminUser,)
    serializer_class = OrderListSerializer
    filterset_fields = ('status',)

    def get_queryset(self) -> list[Order]:
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return self.request.user.orders.all()
