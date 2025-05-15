from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.exceptions import CustomBadRequest
from petshop.utils.permissions import IsAdminUser
from ..selectors import get_all_categories
from ..serializers import ArticleCategorySerializer


@extend_schema(tags=['Article Categories'])
class ArticleCategoriesListAPI(ListAPIView):
    """
    API for listing Categories. Accessible to all users.
    """
    serializer_class = ArticleCategorySerializer
    queryset = get_all_categories()
    permission_classes = (AllowAny,)
    search_fields = ('title',)


@extend_schema(tags=['Article Categories'])
class ArticleCategoryCreateAPI(GenericAPIView):
    """
    API for creating Categories. Accessible only to admins.
    """
    serializer_class = ArticleCategorySerializer
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
