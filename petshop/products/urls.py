from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('', views.ProductCategoriesListAPI.as_view(), name='categories-list'),
]
