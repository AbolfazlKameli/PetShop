from django.urls import path, include, re_path

from .apis import categories, products, details, images

app_name = 'products'

categories_paths = [
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

details_paths = [
    path('create/', details.ProductDetailCreateAPI.as_view(), name='detail-create'),
    path('<int:detail_id>/update/', details.ProductDetailUpdateAPI.as_view(), name='detail-update'),
    path('<int:detail_id>/delete/', details.ProductDetailDeleteAPI.as_view(), name='detail-delete'),
]

images_paths = [
    path('create/', images.ProductImageCreateAPI.as_view(), name='image-create'),
    path('<int:image_id>/update/', images.ProductImageUpdateAPI.as_view(), name='image-update'),
    path('<int:image_id>/delete/', images.ProductImageDeleteAPI.as_view(), name='image-delete'),
]

urlpatterns = [
    path('categories/', include(categories_paths)),
    path('', products.ProductsListAPI.as_view(), name='products-list'),
    path('create/', products.ProductCreateAPI.as_view(), name='product-create'),
    path('<int:product_id>/update/', products.ProductUpdateAPI.as_view(), name='product-update'),
    path('<int:product_id>/delete/', products.ProductDeleteAPI.as_view(), name='product-delete'),
    path('<int:product_id>/', products.ProductRetrieveAPI.as_view(), name='product-retrieve'),
    path('<int:product_id>/details/', include(details_paths)),
    path('<int:product_id>/images/', include(images_paths)),
]
