from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from petshop.utils.exceptions import CustomNotFound
from petshop.utils.permissions import IsAdminUser
from ..selectors import get_product_by_id, get_detail_by_id
from ..serializers import ProductDetailsSerializer


class ProductDetailCreateAPI(GenericAPIView):
    serializer_class = ProductDetailsSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = get_product_by_id(kwargs.get('product_id'))
            if product is not None:
                serializer.save(product=product)
                return Response(
                    data={'data': {'message': 'Detail added successfully to the product.'}},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                data={'data': {'message': 'Product not found.'}},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductDetailUpdateAPI(GenericAPIView):
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

    def put(self, request, *args, **kwargs):
        detail = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=detail)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'Detail updated successfully.'}},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )
