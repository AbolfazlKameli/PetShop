from django.urls import path, include, re_path

from .apis import categories, products

app_name = 'products'

categories = [
    path('', categories.ProductCategoriesListAPI.as_view(), name='categories-list'),
    path('create/', categories.ProductCategoryCreateAPI.as_view(), name='category-create'),
    re_path(
        r'(?P<category_slug>[-\w]+)/update/',
        categories.ProductCategoryUpdateAPI.as_view(),
        name='category-update'
    ),
    re_path(
        r'(?P<category_slug>[-\w]+)/delete/',
        categories.ProductCategoryDeleteAPI.as_view(),
        name='category-delete'
    ),
]

urlpatterns = [
    path('categories/', include(categories)),
    path('', products.ProductsListAPI.as_view(), name='products-list'),
]
