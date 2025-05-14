from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.exceptions import CustomBadRequest, CustomNotFound
from ..selectors import get_product_by_id
from ..serializers import ProductReviewSerializer


@extend_schema(tags=['Product Reviews'])
class ProductReviewCreateAPI(GenericAPIView):
    """
    API for creating ProductReviews. Accessible to authenticated users.
    """
    serializer_class = ProductReviewSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses={201: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        product = get_product_by_id(kwargs.get('product_id'))
        if product is None:
            raise CustomNotFound('Product not found.')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, owner=request.user)
            return Response(
                data={'data': {'message': 'Review created successfully.'}},
                status=status.HTTP_201_CREATED
            )
        raise CustomBadRequest(serializer.errors)
