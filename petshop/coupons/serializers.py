from rest_framework import serializers

from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    is_expired = serializers.SerializerMethodField()

    def get_is_expired(self, obj) -> bool:
        return obj.is_expired

    class Meta:
        model = Coupon
        fields = '__all__'
