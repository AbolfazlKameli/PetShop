from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from petshop.utils.permissions import IsAdminUser
from .filters import CouponFilter
from .selectors import get_all_coupons
from .serializers import CouponSerializer


class CouponsListAPI(ListAPIView):
    """
    API for listing Coupons. Accessible only to the admins.
    """
    serializer_class = CouponSerializer
    permission_classes = (IsAdminUser,)
    queryset = get_all_coupons()
    filterset_class = CouponFilter


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
