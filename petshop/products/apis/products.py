from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.permissions import IsAdminUser
from ..filters import ProductFilter
from ..selectors import get_all_products
from ..serializers import ProductListSerializer, ProductSerializer, ProductWriteSerializer
from ..services import create_product


class ProductsListAPI(ListAPIView):
    """
    API for listing products. Accessible to all users.
    """
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)
    queryset = get_all_products()
    filterset_class = ProductFilter
    filterset_fields = ('available', 'category')
    search_fields = ('title', 'description')


class ProductRetrieveAPI(GenericAPIView):
    """
    API for retrieving products by their IDs. Accessible to all users.
    """
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    queryset = get_all_products()
    lookup_url_kwarg = 'product_id'
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.serializer_class(instance=product)
        return Response(
            data={'data': serializer.data},
            status=status.HTTP_200_OK
        )


class ProductCreateAPI(GenericAPIView):
    """
    API for creating products. Accessible only to the admins.
    """
    serializer_class = ProductWriteSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(responses={201: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            category = serializer.validated_data.pop('category')
            create_product(serializer.validated_data, category)
            return Response(
                data={'data': {'message': 'Product saved successfully.'}},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductUpdateAPI(GenericAPIView):
    """
    API for updating products. Accessible only to the admins.
    """
    serializer_class = ProductWriteSerializer
    permission_classes = (IsAdminUser,)
    queryset = get_all_products()
    lookup_url_kwarg = 'product_id'

    @extend_schema(responses={200: ResponseSerializer})
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'Product updated sucessfully.'}},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductDeleteAPI(GenericAPIView):
    """
    API for deleting products. Accessible only to the admins.
    """
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)
    queryset = get_all_products()
    lookup_url_kwarg = 'product_id'

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
