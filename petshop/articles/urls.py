from django.urls import path

from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticlesListAPI.as_view(), name='article'),
]
