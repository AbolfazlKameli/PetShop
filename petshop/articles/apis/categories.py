from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

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
