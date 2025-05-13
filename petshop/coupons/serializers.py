from rest_framework import serializers

from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()

    def get_is_valid(self, obj) -> bool:
        return obj.is_valid

    class Meta:
        model = Coupon
        fields = '__all__'
