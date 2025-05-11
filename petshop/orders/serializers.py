from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    total_quantity = serializers.SerializerMethodField(read_only=True)

    def get_total_price(self, obj):
        return obj.get_total_price()

    def get_total_quantity(self, obj):
        return obj.get_total_quantity()

    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status', 'discount_percent', 'created_date', 'updated_date', 'owner')
