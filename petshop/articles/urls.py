from django.urls import path, include

from .apis import categories

app_name = 'articles'

categories_paths = [
    path('', categories.ArticleCategoriesListAPI.as_view(), name='categories-list'),
    path('create/', categories.ArticleCategoryCreateAPI.as_view(), name='category-create'),
    path('<int:category_id>/update/', categories.ArticleCategoryUpdateAPI.as_view(), name='category-update'),
    path('<int:category_id>/delete/', categories.ArticleCategoryDeleteAPI.as_view(), name='category-delete'),
]

urlpatterns = [
    path('categories/', include(categories_paths)),
]
