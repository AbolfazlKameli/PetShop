from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.UserOrdersListAPI.as_view(), name='user-orders-list'),
    path('<int:order_id>/', views.OrderRetrieveAPI.as_view(), name='order-retrieve'),
    path('<int:order_id>/cancel/', views.OrderCancelAPI.as_view(), name='order-cancel'),
    path('<int:order_id>/accept/', views.OrderAcceptAPI.as_view(), name='order-accept'),
    path('create/', views.OrderCreateAPI.as_view(), name='order-create'),
]
