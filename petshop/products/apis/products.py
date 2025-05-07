from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from ..filters import ProductFilter
from ..selectors import get_all_products
from ..serializers import ProductListSerializer


class ProductsListAPI(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)
    queryset = get_all_products()
    filterset_class = ProductFilter
    filterset_fields = ('available', 'category')
    search_fields = ('title', 'description')
