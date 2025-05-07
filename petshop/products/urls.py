from django.urls import path, include

from . import views

app_name = 'products'

categories = [
    path('', views.ProductCategoriesListAPI.as_view(), name='categories-list'),
    path('create/', views.ProductCategoryCreateAPI.as_view(), name='category-create'),
]

urlpatterns = [
    path('categories/', include(categories)),
]
