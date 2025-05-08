from rest_framework import serializers

from .models import ProductCategory, Product, ProductDetail
from .selectors import get_all_categories


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('title',)


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = ('key', 'value')


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'unit_price', 'final_price', 'discount_percent', 'available')


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    details = ProductDetailsSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = ('slug',)


class ProductWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=get_all_categories(),
        slug_field='title',
        required=True
    )

    class Meta:
        model = Product
        exclude = ('slug', 'final_price', 'available')
