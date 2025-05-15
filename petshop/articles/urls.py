from django.urls import path, include

from .apis import categories

app_name = 'articles'

categories_paths = [
    path('', categories.ArticleCategoriesListAPI.as_view(), name='categories-list'),
    path('create/', categories.ArticleCategoryCreateAPI.as_view(), name='category-create'),
    path('<int:category_id>/update/', categories.ArticleCategoryUpdateAPI.as_view(), name='category-update'),
]

urlpatterns = [
    path('categories/', include(categories_paths)),
]
