from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.exceptions import CustomNotFound, CustomBadRequest
from petshop.utils.permissions import IsAdminUser
from ..selectors import get_product_by_id, get_detail_by_id
from ..serializers import ProductDetailsSerializer, ProductDetailCreateSerializer
from ..services import create_product_details


@extend_schema(tags=['Product Details'])
class ProductDetailCreateAPI(GenericAPIView):
    """
    API for creating product details. Accessible only to the admins.
    """
    serializer_class = ProductDetailCreateSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(responses={201: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = get_product_by_id(kwargs.get('product_id'))
            if product is not None:
                create_product_details(product, serializer.validated_data.get('details'))
                return Response(
                    data={'data': {'message': 'Detail added successfully to the product.'}},
                    status=status.HTTP_201_CREATED
                )
            raise CustomNotFound('Product not found.')
        raise CustomBadRequest(serializer.errors)


@extend_schema(tags=['Product Details'])
class ProductDetailUpdateAPI(GenericAPIView):
    """
    API for updating product details. Accessible only to the amdins.
    """
    serializer_class = ProductDetailsSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        product = get_product_by_id(self.kwargs.get('product_id'))
        if product is None:
            raise CustomNotFound('Product not found.')

        detail = get_detail_by_id(self.kwargs.get('detail_id'))
        if detail is None:
            raise CustomNotFound('Detail not found.')

        return detail

    @extend_schema(responses={200: ResponseSerializer})
    def put(self, request, *args, **kwargs):
        detail = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=detail)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'Detail updated successfully.'}},
                status=status.HTTP_200_OK
            )
        raise CustomBadRequest(serializer.errors)


@extend_schema(tags=['Product Details'])
class ProductDetailDeleteAPI(GenericAPIView):
    """
    API for deleting product details. Accessible only to the admins.
    """
    serializer_class = ProductDetailsSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        product = get_product_by_id(self.kwargs.get('product_id'))
        if product is None:
            raise CustomNotFound('Product not found.')

        detail = get_detail_by_id(self.kwargs.get('detail_id'))
        if detail is None:
            raise CustomNotFound('Detail not found.')

        return detail

    def delete(self, request, *args, **kwargs):
        detail = self.get_object()
        detail.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
