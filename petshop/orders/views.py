from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.exceptions import CustomBadRequest, CustomNotFound
from petshop.utils.permissions import IsOwnerOrAdminUser, IsAdminUser
from .choices import ORDER_STATUS_PENDING
from .selectors import get_all_orders, get_order_by_id, check_order_status, nothing_orders
from .serializers import OrderSerializer, OrderListSerializer, OrderCreateSerializer
from .services import create_order, cancel_order, accept_order


class OrderRetrieveAPI(GenericAPIView):
    """
    API for retrieving authenticated user orders. Accessible only to the users themselves or admins.
    """
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
    """
    API for listing authenticated user orders. Accessible only to the users themselves or admins.
    """
    permission_classes = (IsOwnerOrAdminUser,)
    serializer_class = OrderListSerializer
    filterset_fields = ('status',)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return nothing_orders()
        return self.request.user.orders.all()


class OrdersListAPI(ListAPIView):
    """
    API for listing all orders. Accessible only to the admins.
    """
    permission_classes = (IsAdminUser,)
    serializer_class = OrderListSerializer
    queryset = get_all_orders()
    filterset_fields = ('status',)


class OrderCreateAPI(GenericAPIView):
    """
    API for creating an order for authenticated user. Accessibleo only to authenticated users.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderCreateSerializer

    @extend_schema(responses={201: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            create_order(request.user, serializer.validated_data.get('items'))
            return Response(
                data={'data': {'message': 'Order created successfully.'}},
                status=status.HTTP_201_CREATED
            )
        raise CustomBadRequest(serializer.errors)


class OrderCancelAPI(GenericAPIView):
    """
    API for canceling an order. Accessible only to order owner or admins.
    """
    permission_classes = (IsOwnerOrAdminUser,)
    lookup_url_kwarg = 'order_id'
    serializer_class = OrderSerializer
    allowed_statuses = [ORDER_STATUS_PENDING]

    def get_object(self):
        order = get_order_by_id(self.kwargs.get('order_id'))
        if order is None or not check_order_status(order, self.allowed_statuses):
            raise CustomNotFound('Could`nt find any pending order with this id.')

        self.check_object_permissions(self.request, order)

        return order

    @extend_schema(responses={200: ResponseSerializer})
    def get(self, request, *args, **kwargs):
        order = self.get_object()
        cancel_order(order)
        return Response(
            data={'data': {'message': 'Order cancelled successfully.'}},
            status=status.HTTP_200_OK
        )


class OrderAcceptAPI(GenericAPIView):
    """
    API for accepting orders. Accessible only to admins.
    """
    permission_classes = (IsAdminUser,)
    serializer_class = OrderSerializer
    lookup_url_kwarg = 'order_id'
    allowed_statuses = [ORDER_STATUS_PENDING]

    def get_object(self):
        order = get_order_by_id(self.kwargs.get('order_id'))
        if order is None or not check_order_status(order, self.allowed_statuses):
            raise CustomNotFound('Could`nt find any pending order with this id.')

        self.check_object_permissions(self.request, order)

        return order

    @extend_schema(responses={200: ResponseSerializer})
    def get(self, request, *args, **kwargs):
        order = self.get_object()
        accept_order(order)
        return Response(
            data={'data': {'message': 'Order accepted successfully.'}},
            status=status.HTTP_200_OK
        )
