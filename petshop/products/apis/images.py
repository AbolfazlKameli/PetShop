from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.exceptions import CustomNotFound, CustomBadRequest
from petshop.utils.permissions import IsAdminUser
from ..selectors import get_product_by_id, get_image_by_id
from ..serializers import ProductImageSerializer


class ProductImageCreateAPI(GenericAPIView):
    """
    API for creating product images. Accessible only to the admins.
    """
    serializer_class = ProductImageSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(responses={201: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        product = get_product_by_id(kwargs.get('product_id'))
        if product is None:
            raise CustomNotFound('Product not found.')
        serializer = self.serializer_class(data=request.data, context={'product': product})
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(
                data={'data': {'message': 'Image added successfully to the product.'}},
                status=status.HTTP_201_CREATED
            )
        raise CustomBadRequest(serializer.errors)


class ProductImageUpdateAPI(GenericAPIView):
    """
    API for updating product images. Accessible only th admins.
    """
    serializer_class = ProductImageSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        product = get_product_by_id(self.kwargs.get('product_id'))
        if product is None:
            raise CustomNotFound('Product not found.')

        image = get_image_by_id(self.kwargs.get('image_id'))
        if image is None:
            raise CustomNotFound('Image not found.')

        return image, product

    @extend_schema(responses={200: ResponseSerializer})
    def put(self, request, *args, **kwargs):
        image, product= self.get_object()
        serializer = self.serializer_class(data=request.data, instance=image, context={'product': product})
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'Image updated successfully.'}},
                status=status.HTTP_200_OK
            )
        raise CustomBadRequest(serializer.errors)
