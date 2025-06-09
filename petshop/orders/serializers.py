from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj) -> int:
        return obj.get_total_price()

    class Meta:
        model = OrderItem
        exclude = ('order',)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    total_quantity = serializers.SerializerMethodField(read_only=True)

    def get_total_price(self, obj) -> int:
        return obj.get_total_price()

    def get_total_quantity(self, obj) -> int:
        return obj.get_total_quantity()

    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status', 'discount_percent', 'created_date', 'updated_date', 'owner')


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('items',)

    def validate(self, attrs):
        items = attrs.get('items')[0]
        product = items.get('product')
        quantity = items.get('quantity')

        if not items:
            raise serializers.ValidationError({'items': 'There is no items in data.'})

        if not product.available:
            raise serializers.ValidationError({'items': [{'product': ['This product is out of stock.']}]})

        if product.quantity < quantity or quantity <= 0:
            raise serializers.ValidationError({
                'items': [
                    {'quantity': ['The quantity you requested is more than what is currently available in stock.']}
                ]
            })

        if quantity > 100:
            raise serializers.ValidationError({
                'items': [
                    {'quantity': ['You can`t order more than 100 products.']}
                ]
            })

        return attrs
