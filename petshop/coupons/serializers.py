from rest_framework import serializers

from petshop.orders.selectors import get_pending_orders
from .models import Coupon
from .selectors import get_valid_coupons


class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()

    def get_is_valid(self, obj) -> bool:
        return obj.is_valid

    class Meta:
        model = Coupon
        fields = '__all__'


class CouponApplySerializer(serializers.Serializer):
    coupon = serializers.SlugRelatedField(
        slug_field='code',
        queryset=get_valid_coupons(),
        write_only=True,
        required=True
    )
    order = serializers.PrimaryKeyRelatedField(queryset=get_pending_orders(), write_only=True, required=True)

    def validate_order(self, data):
        if data.coupon is not None:
            raise serializers.ValidationError('You can`t apply more than one coupon on an order.')
        return data


class CouponDiscardSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=get_pending_orders(), write_only=True, required=True)

    def validate_order(self, data):
        if data.coupon is None:
            raise serializers.ValidationError('This order does`nt have any coupons.')
        return data
