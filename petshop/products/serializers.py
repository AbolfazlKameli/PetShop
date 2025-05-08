from rest_framework import serializers

from .models import ProductCategory, Product, ProductDetail, ProductImage
from .selectors import get_all_categories, get_primary_image, get_latest_image


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'title')


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = ('id', 'key', 'value')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'is_primary')

    def validate_is_primary(self, data):
        product = self.context.get('product')
        primary_image = get_primary_image(product=product)
        if primary_image is not None and data:
            raise serializers.ValidationError('You cant choose two primary images for one product.')
        return data


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    def get_image(self, obj):
        primary_image = get_primary_image(product=obj)
        if primary_image is None:
            primary_image = get_latest_image(product=obj)
        return ProductImageSerializer(instance=primary_image).data

    class Meta:
        model = Product
        fields = ('id', 'title', 'unit_price', 'final_price', 'discount_percent', 'available', 'image')


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    details = ProductDetailsSerializer(read_only=True, many=True)
    images = ProductImageSerializer(many=True, read_only=True)

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
