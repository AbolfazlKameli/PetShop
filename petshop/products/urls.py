from django.urls import path, include, re_path

from .apis import categories, products, details

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

details = [
    path('create/', details.ProductDetailCreateAPI.as_view(), name='detail-create'),
]

urlpatterns = [
    path('categories/', include(categories)),
    path('', products.ProductsListAPI.as_view(), name='products-list'),
    path('create/', products.ProductCreateAPI.as_view(), name='product-create'),
    path('<int:product_id>/update/', products.ProductUpdateAPI.as_view(), name='product-update'),
    path('<int:product_id>/delete/', products.ProductDeleteAPI.as_view(), name='product-delete'),
    path('<int:product_id>/', products.ProductRetrieveAPI.as_view(), name='product-retrieve'),
    path('<int:product_id>/details/', include(details)),
]
