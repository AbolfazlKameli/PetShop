from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.exceptions import CustomBadRequest
from petshop.utils.permissions import IsAdminUser
from .selectors import get_all_articles
from .serializers import ArticlesListSerializer, ArticleSerializer


class ArticlesListAPI(ListAPIView):
    """
    API for listing Articles. Accessible to all users.
    """
    serializer_class = ArticlesListSerializer
    permission_classes = (AllowAny,)
    queryset = get_all_articles()
    search_fields = ('title', 'text')


class ArticleRetrieveAPI(GenericAPIView):
    """
    API for retrieving Articles. Accessible to all users.
    """
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    queryset = get_all_articles()
    lookup_url_kwarg = 'article_id'

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        serializer = self.serializer_class(instance=article)
        return Response(
            data={'data': serializer.data},
            status=status.HTTP_200_OK
        )


class ArticleCreateAPI(GenericAPIView):
    """
    API for creating Articles. Accessible only to the admins.
    """
    serializer_class = ArticleSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(responses={201: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'Article created successfully.'}},
                status=status.HTTP_201_CREATED
            )
        raise CustomBadRequest(serializer.errors)


class ArticleUpdateAPI(GenericAPIView):
    """
    API for updating Articles. Accessible only to the admins.
    """
    serializer_class = ArticleSerializer
    permission_classes = (IsAdminUser,)
    queryset = get_all_articles()
    lookup_url_kwarg = 'article_id'

    @extend_schema(responses={200: ResponseSerializer})
    def put(self, request, *args, **kwargs):
        article = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=article)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'Article updated successfully.'}},
                status=status.HTTP_200_OK
            )
        raise CustomBadRequest(serializer.errors)
