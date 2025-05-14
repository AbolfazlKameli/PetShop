from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.exceptions import CustomBadRequest, CustomNotFound
from petshop.utils.permissions import IsAdminUser
from ..selectors import get_product_by_id, get_review_by_product_and_id
from ..serializers import ProductReviewSerializer, ReviewChangeStatusSerializer
from ..services import change_review_status


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


@extend_schema(tags=['Product Reviews'])
class ProductReviewStatusChangeAPI(GenericAPIView):
    """
    API for approving or rejecting Reviews. Accessible only to the admins.
    """
    serializer_class = ReviewChangeStatusSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        product = get_product_by_id(self.kwargs.get('product_id'))
        if product is None:
            raise CustomNotFound('Product not found.')

        review = get_review_by_product_and_id(product, self.kwargs.get('review_id'))
        if review is None:
            raise CustomNotFound('Review not found.')

        return review

    @extend_schema(responses={200: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            change_review_status(review, serializer.validated_data.get('status'))
            return Response(
                data={'data': {'message': 'Status change successfully.'}},
                status=status.HTTP_200_OK
            )
        raise CustomBadRequest(serializer.errors)
