from django.urls import path, include, re_path

from . import views

app_name = 'products'

categories = [
    path('', views.ProductCategoriesListAPI.as_view(), name='categories-list'),
    path('create/', views.ProductCategoryCreateAPI.as_view(), name='category-create'),
    re_path(r'(?P<category_slug>[-\w]+)/update/', views.ProductCategoryUpdateAPI.as_view(), name='category-update'),
    re_path(r'(?P<category_slug>[-\w]+)/delete/', views.ProductCategoryDeleteAPI.as_view(), name='category-delete'),
]

urlpatterns = [
    path('categories/', include(categories)),
]
