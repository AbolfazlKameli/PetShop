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
        errors = []
        for index, item in enumerate(attrs.get('items', [])):
            item_errors = {}
            if not item:
                errors.append({index: 'There is no items in data.'})
                continue

            product = item.get('product')
            quantity = item.get('quantity')

            if not product.available:
                item_errors['product'] = 'This product is out of stock.'

            if quantity is None or quantity <= 0:
                item_errors['quantity'] = 'The quantity should be greater than zero.'

            if product.quantity < quantity:
                item_errors['quantity'] = 'The quantity you have entered is less than the product quantity.'

            if quantity > 100:
                item_errors['quantity'] = 'The quantity you have entered is greater than 100.'

            if item_errors:
                errors.append({index: item_errors})
        if errors:
            raise serializers.ValidationError(errors)

        return attrs
