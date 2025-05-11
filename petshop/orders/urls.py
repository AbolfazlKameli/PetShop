from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.UserOrdersListAPI.as_view(), name='user-orders-list'),
    path('<int:order_id>/', views.OrderRetrieveAPI.as_view(), name='order-retrieve'),
]
