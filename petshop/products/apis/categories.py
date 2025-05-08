from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.exceptions import CustomBadRequest
from petshop.utils.permissions import IsAdminUser
from ..selectors import get_all_categories
from ..serializers import ProductCategorySerializer


class ProductCategoriesListAPI(ListAPIView):
    """
    API for listing Categories. Accessible to all users.
    """
    serializer_class = ProductCategorySerializer
    queryset = get_all_categories()
    permission_classes = (AllowAny,)
    search_fields = ('title',)


class ProductCategoryCreateAPI(GenericAPIView):
    """
    API for creating Categories. Accessible only to the admins.
    """
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(responses={201: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'Category created successfully.'}},
                status=status.HTTP_201_CREATED
            )
        raise CustomBadRequest(serializer.errors)


class ProductCategoryUpdateAPI(GenericAPIView):
    """
    API for updating Categories. Accessible only to the admins.
    """
    serializer_class = ProductCategorySerializer
    queryset = get_all_categories()
    permission_classes = (IsAdminUser,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'category_slug'

    @extend_schema(responses={200: ResponseSerializer})
    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=category)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'Category updated successfully.'}},
                status=status.HTTP_201_CREATED
            )
        raise CustomBadRequest(serializer.errors)


class ProductCategoryDeleteAPI(GenericAPIView):
    """
    API for deleting Categories. Accessible only to the admins.
    """
    serializer_class = ProductCategorySerializer
    queryset = get_all_categories()
    permission_classes = (IsAdminUser,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'category_slug'

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
