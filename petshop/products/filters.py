import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='iexact')
    min_price = django_filters.NumberFilter(field_name='final_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='final_price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('available', 'category', 'min_price', 'max_price')
