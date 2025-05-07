from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from petshop.utils.permissions import IsAdminUser
from .selectors import get_all_categories
from .serializers import ProductCategorySerializer


class ProductCategoriesListAPI(ListAPIView):
    serializer_class = ProductCategorySerializer
    queryset = get_all_categories()
    permission_classes = (AllowAny,)
    search_fields = ('title',)


class ProductCategoryCreateAPI(GenericAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'Category created successfully.'}},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'data': {'errors': serializer.errors}},
            status=status.HTTP_400_BAD_REQUEST
        )
