from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from petshop.utils.exceptions import CustomBadRequest
from petshop.utils.permissions import IsOwnerOrAdminUser
from .models import Order
from .selectors import get_all_orders
from .serializers import OrderSerializer, OrderListSerializer, OrderCreateSerializer
from .services import create_order


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


class OrderCreateAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            create_order(request.user, serializer.validated_data.get('items'))
            return Response(
                data={'data': {'message': 'Order created successfully.'}},
                status=status.HTTP_201_CREATED
            )
        raise CustomBadRequest(serializer.errors)
