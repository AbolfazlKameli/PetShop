from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.exceptions import CustomBadRequest
from petshop.utils.permissions import IsAdminUser, IsOwnerOrAdminUser
from .filters import CouponFilter
from .selectors import get_all_coupons, get_valid_coupons
from .serializers import CouponSerializer, CouponApplySerializer, CouponDiscardSerializer
from .services import discard_coupon, apply_coupon


@extend_schema(tags=['Coupons'])
class CouponsListAPI(ListAPIView):
    """
    API for listing Coupons. Accessible only to the admins.
    """
    serializer_class = CouponSerializer
    permission_classes = (IsAdminUser,)
    queryset = get_all_coupons()
    filterset_class = CouponFilter


@extend_schema(tags=['Coupons'])
class CouponRetrieveAPI(GenericAPIView):
    """
    API for retrieving Coupon objects. Accessible only to the admins.
    """
    serializer_class = CouponSerializer
    permission_classes = (IsAdminUser,)
    queryset = get_all_coupons()
    lookup_url_kwarg = 'coupon_id'

    def get(self, request, *args, **kwargs):
        coupon = self.get_object()
        serializer = self.serializer_class(instance=coupon)
        return Response(
            data={'data': serializer.data},
            status=status.HTTP_200_OK
        )


@extend_schema(tags=['Coupons'])
class CouponCreateAPI(GenericAPIView):
    """
    API for creating Coupons. Accessible only to admins.
    """
    serializer_class = CouponSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(responses={201: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'Coupon created successfully.'}},
                status=status.HTTP_201_CREATED
            )
        raise CustomBadRequest(serializer.errors)


@extend_schema(tags=['Coupons'])
class CouponUpdateAPI(GenericAPIView):
    """
    API for updating valid Coupons. Accessible only to the admins.
    """
    serializer_class = CouponSerializer
    permission_classes = (IsAdminUser,)
    lookup_url_kwarg = 'coupon_id'
    queryset = get_valid_coupons()

    @extend_schema(responses={200: ResponseSerializer})
    def put(self, request, *args, **kwargs):
        coupon = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=coupon)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'Coupon updated successfully.'}},
                status=status.HTTP_200_OK
            )
        raise CustomBadRequest(serializer.errors)


@extend_schema(tags=['Coupons'])
class CouponDeleteAPI(GenericAPIView):
    """
    API for deleting Coupons. Accessible only to the admins.
    """
    serializer_class = CouponSerializer
    permission_classes = (IsAdminUser,)
    lookup_url_kwarg = 'coupon_id'
    queryset = get_all_coupons()

    def delete(self, request, *args, **kwargs):
        coupon = self.get_object()
        discard_coupon(coupon, coupon.orders.all())
        coupon.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


@extend_schema(tags=['Coupons'])
class CouponApplyAPI(GenericAPIView):
    """
    API for applying Coupons to orders. Accessible to orders owners or admins.
    """
    serializer_class = CouponApplySerializer
    permission_classes = (IsOwnerOrAdminUser,)

    @extend_schema(responses={200: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data.get('order')
            coupon = serializer.validated_data.get('coupon')
            self.check_object_permissions(request, order)

            apply_coupon(order=order, coupon=coupon)

            return Response(
                data={'data': {'message': 'Coupon applied successfully.'}},
                status=status.HTTP_200_OK
            )
        raise CustomBadRequest(serializer.errors)


@extend_schema(tags=['Coupons'])
class CouponDiscardAPI(GenericAPIView):
    """
    API for discarding Coupons. Accessible to orders owners and admins.
    """
    serializer_class = CouponDiscardSerializer
    permission_classes = (IsOwnerOrAdminUser,)

    @extend_schema(responses={200: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data.get('order')
            coupon = order.coupon

            self.check_object_permissions(request, order)

            discard_coupon(coupon, [order])

            return Response(
                data={'data': {'message': 'Coupon discarded successfully.'}},
                status=status.HTTP_200_OK
            )
        raise CustomBadRequest(serializer.errors)
