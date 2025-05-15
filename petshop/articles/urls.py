from django.urls import path, include

from .apis import categories

app_name = 'articles'

categories_paths = [
    path('', categories.ArticleCategoriesListAPI.as_view(), name='categories-list'),
]

urlpatterns = [
    path('categories/', include(categories_paths)),
]
