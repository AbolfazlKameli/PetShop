from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .selectors import get_all_categories
from .serializers import ProductCategorySerializer


class ProductCategoriesListAPI(ListAPIView):
    serializer_class = ProductCategorySerializer
    queryset = get_all_categories()
    permission_classes = (AllowAny,)
    search_fields = ('title',)
