from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .selectors import get_all_articles
from .serializers import ArticlesListSerializer


class ArticlesListAPI(ListAPIView):
    """
    API for listing Articles. Accessible to all users.
    """
    serializer_class = ArticlesListSerializer
    permission_classes = (AllowAny,)
    queryset = get_all_articles()
    search_fields = ('title', 'text')
