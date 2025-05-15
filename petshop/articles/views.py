from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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
