from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..filters import ProductFilter
from ..selectors import get_all_products
from ..serializers import ProductListSerializer, ProductSerializer


class ProductsListAPI(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)
    queryset = get_all_products()
    filterset_class = ProductFilter
    filterset_fields = ('available', 'category')
    search_fields = ('title', 'description')


class ProductRetrieveAPI(GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    queryset = get_all_products()
    lookup_url_kwarg = 'product_slug'
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.serializer_class(instance=product)
        return Response(
            data={'data': serializer.data},
            status=status.HTTP_200_OK
        )
