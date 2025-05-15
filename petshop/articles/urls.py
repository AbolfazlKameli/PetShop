from django.urls import path

from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticlesListAPI.as_view(), name='articles-list'),
    path('<int:article_id>/', views.ArticleRetrieveAPI.as_view(), name='article-retrieve'),
    path('create/', views.ArticleCreateAPI.as_view(), name='article-create'),
]
